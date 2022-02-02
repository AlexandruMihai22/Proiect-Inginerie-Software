import os
import sqlite3
import tempfile

import pytest
import json

import db
import status
from app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(testing=True, db_path=db_path)

    with app.app_context():
        db.close_db()
        db.init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    db_fd, db_path = tempfile.mkstemp()
    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client
    os.close(db_fd)
    os.unlink(db_path)


@pytest.mark.integtest
def test_app(app, client):
    with app.app_context():
        # Register
        response = client.post('/auth/register', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200

        # Login
        response = client.post('auth/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200

        # Set temperature
        rv = client.post('/system_temperature/set', data={'temp': 100}, follow_redirects=True)
        assert rv.status_code == 200

        # Set moisture
        rv = client.post('/soil_moisture/set', data={'soil_moisture': 60}, follow_redirects=True)
        assert rv.status_code == 200

        # Set watering
        rv = client.post('/watering', data={'water_quantity': 40}, follow_redirects=True)
        assert rv.status_code == 200

        # Water status, quantity should be 0
        response = status.get_status()
        assert response['status'] == 'The plant was successfully watered' and response['data']['water_quantity'] == 0

        # Logout
        response = client.get('/auth/logout')
        assert response.status_code == 200
