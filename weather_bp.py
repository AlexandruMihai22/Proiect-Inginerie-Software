from flask import (
    Blueprint, request, jsonify
)
from auth import login_required
from db import get_db
import weather

bp = Blueprint('weather', __name__, url_prefix='/weather')


@bp.route('/temperature', methods=['GET'])
@login_required
def get_temperature():
    return weather.get_temperature_from_weather_api(), 200

@bp.route('/humidity', methods=['GET'])
@login_required
def get_humidity():
    return weather.get_humidity_from_weather_api()