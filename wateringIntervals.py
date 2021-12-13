#import sched, time
from time import time, sleep

from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from db import get_db

bp = Blueprint('watering/intervals', __name__, url_prefix='/watering/intervals')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def set_watering():
    if request.method == 'POST':
        water_quantity = request.form['water_quantity']
        total_water_quantity = request.form['total_water_quantity']
        interval = request.form['interval']


        if not water_quantity:
            return jsonify({'status': 'Water quantity is required.'}), 403

        if not total_water_quantity:
            return jsonify({'status': 'Total water quantity is required.'}), 403

        if not interval:
            return jsonify({'status': 'Interval is required.'}), 403

        db = get_db()

        print(total_water_quantity)

        total_water_quantity = int(total_water_quantity)
        water_quantity = int(water_quantity)
        interval = int(interval)


        while total_water_quantity - water_quantity >= 0:
            total_water_quantity -= water_quantity
            sleep(interval - time() % interval)
            print("hmm")
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
        print("check",check)
        return jsonify({
            'status': 'The plant was successfully watered',
            'data': {
                'id': check['id'],
                'timestamp': check['timestamp'],
                'water_quantity': check['water_quantity']
            }
        }), 200


    if request.method == 'GET':

        # db = get_db()

        water_info = get_db().execute(
            'SELECT id, timestamp, water_quantity'
            ' FROM watering'
        ).fetchall()


        waterJsonList = []
        for i in range(len(water_info)):
            water_json  ={
                'status': 'The plant was successfully watered',
                'data': {
                    'id': water_info[i]['id'],
                    'timestamp': water_info[i]['timestamp'],
                    'water_quantity': water_info[i]['water_quantity']
                }
            }
            waterJsonList.append(water_json)

        response = jsonify(waterJsonList)


        return jsonify(waterJsonList),200

