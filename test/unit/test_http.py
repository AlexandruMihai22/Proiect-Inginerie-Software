import os
import sqlite3
import tempfile

import pytest
import json

import db
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

# -------- DATABASE --------


def test_db_connection(app):
    with app.app_context():
        err = False
        try:
            entry = db.get_db().execute(
                'SELECT 100'
            ).fetchone()

            if not entry:
                err = True

        except sqlite3.Error:
            err = True

        assert not err


# -------- END DATABASE --------


@pytest.fixture
def client(app):
    db_fd, db_path = tempfile.mkstemp()
    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_root_endpoint(client):
    landing = client.get('/')
    html = landing.data.decode()

    assert 'Hello World' in html
    assert landing.status_code == 200


# Register, Login and logout
def register(client, username, password):
    return client.post('/auth/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def login(client, username, password):
    return client.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


# def logout(client):
#     return client.get('/logout', follow_redirects=True)


def test_register_login_logout(client):
    """Make sure register, login and logout works."""

    username = 'test'
    password = 'test'

    rv = register(client, username, password)
    assert b'user registered succesfully' in rv.data

    rv = login(client, username, password)
    assert b'user logged in succesfully' in rv.data

    # rv = logout(client)
    # assert b'You were logged out' in rv.data

    rv = login(client, f'{username}x', password)
    assert b'username not found' in rv.data

    rv = login(client, username, f'{password}x')
    assert b'password is incorrect' in rv.data


def test_get_temperature(client):
    register(client, 'test', 'test')
    login(client, 'test', 'test')
    payload = {'temp': 100}
    client.post('/system_temperature/set', data=payload, follow_redirects=True)
    request = client.get('/system_temperature/')
    assert request.status_code == 200


def test_set_temperature(client):
    register(client, 'test', 'test')
    login(client, 'test', 'test')
    payload = {'temp': 100}
    rv = client.post('/system_temperature/set', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res['status'] == "Temperature successfully retrieved."


def test_watering_intervals(client):
    register(client, 'test', 'test')
    login(client, 'test', 'test')
    payload = {'water_quantity': 40, 'total_water_quantity': 120, 'interval': 2}
    rv = client.post('/watering/intervals', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert res.status_code == 200
    assert res['status'] == "The plant was successfully watered."
