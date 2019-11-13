from flask import Blueprint, render_template, request, redirect, url_for

from organizer.db import get_session, init_connection, re_init_schema, init_fake_data

bp = Blueprint('developer', __name__, url_prefix='/developer')


@bp.route('/console')
def console():
    return render_template('admin/console.html')


@bp.route('/console/clear_db')
def clear_db():
    init_connection()
    re_init_schema()
    return redirect(url_for('trips.index'))


@bp.route('/console/fill_fake')
def fill_fake_data():
    init_connection()
    re_init_schema()
    init_fake_data()
    return redirect(url_for('trips.index'))


@bp.route('/console/execute_sql', methods=['POST'])
def execute_sql():
    sql_code = request.form['code']

    with get_session() as session:
        session.execute(sql_code)

    return redirect(url_for('developer.console'))