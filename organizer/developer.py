from flask import Blueprint, render_template, request, redirect, url_for

from organizer.db import get_session
from organizer.auth import login_required_group
from organizer.schema import AccessGroup

bp = Blueprint('developer', __name__, url_prefix='/developer')


@bp.route('/console')
@login_required_group(AccessGroup.Administrator)
def console():
    return render_template('admin/console.html')


@bp.route('/console/execute_sql', methods=['POST'])
@login_required_group(AccessGroup.Administrator)
def execute_sql():
    sql_code = request.form['code']

    with get_session() as session:
        session.execute(sql_code)

    return redirect(url_for('developer.console'))
