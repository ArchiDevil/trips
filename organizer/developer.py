from flask import Blueprint, render_template, request, redirect, url_for

from organizer.db import get_session
from organizer.auth import login_required_group
from organizer.schema import AccessGroup

bp = Blueprint('developer', __name__, url_prefix='/developer')


@bp.get('/console')
@login_required_group(AccessGroup.Administrator)
def console():
    return render_template('admin/console.html')


@bp.post('/console/execute_sql')
@login_required_group(AccessGroup.Administrator)
def execute_sql():
    sql_code = request.form['code']

    with get_session() as session:
        session.execute(sql_code)
        session.commit()

    return redirect(url_for('developer.console'))
