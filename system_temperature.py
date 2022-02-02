from db import get_db

from flask import request, jsonify


def get_system_temperature():
    check = get_db().execute(
        'SELECT id, timestamp, value FROM temperature ORDER BY timestamp DESC'
    ).fetchone()

    if check is None:
        return {'status': "Please set temperature."}

    return jsonify({
        'status': "Temperature successfully retrieved.",
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
        }
    }), 200


def set_system_temperature():
    temp = request.form['temp']
    try:
        float(temp)
    except ValueError:
        return jsonify({'status': 'temperature must be numeric.'}), 422
    if not temp:
        return jsonify({'status': 'Temp is required.'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO temperature (value) VALUES (?)',
        (temp,)
    )
    db.commit()

    return get_system_temperature()
