from db import get_db

from flask import (
    Blueprint, request, jsonify
)


def get_soil_moisture():
    check = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM soil_moisture'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if check is None:
        return {'status': 'Please set soil moisture'}

    return jsonify({
        'status': 'soil moisture successfully retrieved',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
        }
    }), 200


def set_soil_moisture():
    soil_moisture = request.form['soil_moisture']
    error = None
    if not soil_moisture:
        return jsonify({'status': 'soil_moisture is required.'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO soil_moisture (value)'
        'VALUES (?)',
        (soil_moisture,)
    )
    db.commit()

    return get_soil_moisture()