from flask import Blueprint, render_template

from organizer.auth import login_required_group
from organizer.schema import AccessGroup

bp = Blueprint('developer', __name__, url_prefix='/developer')


@bp.get('/administration')
@login_required_group(AccessGroup.Administrator)
def administration():
    return render_template('admin/administration.html')
