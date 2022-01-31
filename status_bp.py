from flask import (
    Blueprint, jsonify, current_app
)

from auth import login_required
from db import get_db
import status

bp = Blueprint('status_bp', __name__, url_prefix='/status')


@bp.route('/', methods=['GET'])
@login_required
def get_status():
    return status.get_status()