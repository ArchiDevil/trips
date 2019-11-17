from flask import Blueprint, render_template, request, redirect, url_for
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
    if request.method == 'POST':
        # check values here
        name = request.form['name']

        password = request.form['password']
        pass_hash = generate_password_hash(password)

        group = request.form['group']
        access_group = AccessGroup[group]

        with get_session() as session:
            session.add(User(name=name, password=pass_hash,
                             access_group=access_group))
            session.commit()

        return redirect(url_for('users.index'))

    return render_template('users/add.html', groups=[x.name for x in AccessGroup])


@bp.route('/remove/<int:user_id>')
@login_required_group(AccessGroup.Administrator)
def delete(user_id):
    with get_session() as session:
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
        return redirect(url_for('users.index'))
