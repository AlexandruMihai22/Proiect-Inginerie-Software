from flask import Blueprint

from auth import login_required
import status as bed_status

bp = Blueprint('status_api', __name__, url_prefix='/status')


@bp.route('/')
@login_required
def get_status_api():
    # TODO Right now default status code is 200, but the correct status code should be received
    # from bed_status.get_status().

    return bed_status.get_status(), 200
