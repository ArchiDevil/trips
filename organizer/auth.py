import functools

from flask import Blueprint, render_template, request, g, redirect, url_for, session, flash, abort
from werkzeug.security import check_password_hash

from organizer.db import get_session
from organizer.schema import User, AccessGroup

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required_group(group):
    def login_required_grouped(view):
        @functools.wraps(view)
        def wrapped_view_grouped(**kwargs):
            if 'user' not in g or g.user is None:
                return redirect(url_for('auth.login'))
            if g.user.access_group.value < group.value:
                abort(403)
            return view(**kwargs)
        return wrapped_view_grouped
    return login_required_grouped


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        with get_session() as sql_session:
            g.user = sql_session.query(User).filter(User.id == user_id).one()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_login = request.form['login']
        form_password = request.form['password']
        form_remember = True if 'remember' in request.form.keys() else False

        with get_session() as sql_session:
            user = sql_session.query(User).filter(User.name == form_login).first()
            if not user:
                flash('No such user')
            elif not check_password_hash(user.password, form_password):
                flash('Incorrect password')
            else: # no issues
                session.clear()
                session['user_id'] = user.id
                session.permanent = form_remember
                return redirect(url_for('trips.index'))

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required_group(AccessGroup.Guest)
def logout():
    session.clear()
    return redirect(url_for('trips.index'))
