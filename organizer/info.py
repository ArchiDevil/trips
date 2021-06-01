from flask import Blueprint, render_template

from organizer.auth import login_required_group
from organizer.schema import AccessGroup

bp = Blueprint('info', __name__)


@bp.route('/info/')
@login_required_group(AccessGroup.Guest)
def index():
    return render_template('info.html')
