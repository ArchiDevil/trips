from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, g
from werkzeug.security import generate_password_hash

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import User, AccessGroup

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@login_required_group(AccessGroup.Administrator)
def index():
    with get_session() as session:
        users = session.query(User).all()
        return render_template('users/users.html', users=users)


@bp.route('/add', methods=['GET', 'POST'])
@login_required_group(AccessGroup.Administrator)
def add():
    groups = [x.name for x in AccessGroup]
    add_page = 'users/add.html'

    if request.method == 'POST':
        name = request.form['name']
        if not name:
            flash('Empty name provided')
            return render_template(add_page, groups=groups)

        password = request.form['password']
        if not password:
            flash('Empty password provided')
            return render_template(add_page, groups=groups)

        pass_hash = generate_password_hash(password)

        group = request.form['group']
        if not group:
            flash('Empty group provided')
            return render_template(add_page, groups=groups)

        try:
            access_group = AccessGroup[group]
        except KeyError:
            flash('Wrong group provided')
            return render_template(add_page, groups=groups)

        with get_session() as session:
            session.add(User(name=name, password=pass_hash,
                             access_group=access_group))
            session.commit()

        return redirect(url_for('users.index'))

    return render_template(add_page, groups=groups)


@bp.route('/remove/<int:user_id>')
@login_required_group(AccessGroup.Administrator)
def delete(user_id):
    with get_session() as session:
        if user_id == g.user.id:
            # it is not possible to remove current user
            abort(403)

        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404)

        session.query(User).filter(User.id == user_id).delete()
        session.commit()
        return redirect(url_for('users.index'))
