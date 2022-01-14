from db import get_db

from flask import (
    Blueprint, request, jsonify
)


def get_system_temperature():
    check = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM temperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Temperature successfully retrieved',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
        }
    }), 200


def set_system_temperature():
    temp = request.form['temp']
    error = None
    if not temp:
        return jsonify({'status': 'Temp is required.'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO temperature (value)'
        'VALUES (?)',
        (temp,)
    )
    db.commit()

    return get_system_temperature()
