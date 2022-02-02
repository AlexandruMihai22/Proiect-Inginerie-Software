from flask import Blueprint
from auth import login_required
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


@bp.route('/precipitation', methods=['GET'])
@login_required
def get_precipitation():
    return weather.get_precipitation_from_weather_api()
