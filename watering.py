from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from db import get_db

bp = Blueprint('watering', __name__, url_prefix='/watering')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def set_watering():
    if request.method == 'POST':
        water_quantity = request.form['water_quantity']
        try:
            float(water_quantity)
        except:
            return jsonify({'status': 'water quantity must be numeric.'}), 422

        if not water_quantity:
            return jsonify({'status': 'Water quantity is required.'}), 403

        db = get_db()
        db.execute(
            'INSERT INTO watering (water_quantity)'
            ' VALUES (?)',
            (water_quantity,)
        )
        db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, water_quantity'
        ' FROM watering'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': 'The plant was successfully watered',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'water_quantity': check['water_quantity']
        }
    }), 200


