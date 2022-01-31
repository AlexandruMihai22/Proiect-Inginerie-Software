from flask import Blueprint

from auth import login_required
import status

bp = Blueprint('status_bp', __name__, url_prefix='/status')


@bp.route('/', methods=['GET'])
@login_required
def get_status():
    return status.get_status()
