from flask import Blueprint
from auth import login_required
import system_temperature

bp = Blueprint('system_temperature_bp', __name__, url_prefix='/system_temperature')


@bp.route('/', methods=['GET'])
@login_required
def get_temperature():
    return system_temperature.get_system_temperature()


@bp.route('/set', methods=['POST'])
@login_required
def set_temperature():
    return system_temperature.set_system_temperature()
