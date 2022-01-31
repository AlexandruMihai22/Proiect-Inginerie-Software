from flask import (
    Blueprint, request, jsonify
)
from auth import login_required
from db import get_db
import soil_moisture

bp = Blueprint('soil_moisture_bp', __name__, url_prefix='/soil_moisture')


@bp.route('/', methods=['GET'])
@login_required
def get_soil_moisture():
    return soil_moisture.get_soil_moisture()


@bp.route('/set', methods=['POST'])
@login_required
def set_soil_moisture():
    return soil_moisture.set_soil_moisture()
