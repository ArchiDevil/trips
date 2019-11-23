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
    add_page = 'users/edit.html'
    form_caption = "Add a user"
    submit_text = 'Add'

    if request.method == 'POST':
        login = request.form['login']
        if not login:
            flash('Empty login provided')
            return render_template(add_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

        password = request.form['password']
        if not password:
            flash('Empty password provided')
            return render_template(add_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

        pass_hash = generate_password_hash(password)

        group = request.form['group']
        if not group:
            flash('Empty group provided')
            return render_template(add_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

        try:
            access_group = AccessGroup[group]
        except KeyError:
            flash('Wrong group provided')
            return render_template(add_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

        with get_session() as session:
            user = session.query(User).filter(User.login == login).first()
            if user:
                flash('User with the same login already exists')
                return render_template(add_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

            session.add(User(login=login, password=pass_hash,
                             access_group=access_group))
            session.commit()

        return redirect(url_for('users.index'))

    return render_template(add_page, groups=groups, form_caption=form_caption, submit_text=submit_text)


@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required_group(AccessGroup.Administrator)
def edit(user_id):
    groups = [x.name for x in AccessGroup]
    edit_page = 'users/edit.html'
    form_caption = "Edit a user"
    submit_text = 'Edit'

    if request.method == 'POST':
        login = request.form['login']
        if not login:
            flash('Empty login provided')
            return render_template(edit_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

        group = request.form['group']
        if not group:
            flash('Empty group provided')
            return render_template(edit_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

        try:
            access_group = AccessGroup[group]
        except KeyError:
            flash('Wrong group provided')
            return render_template(edit_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

        with get_session() as session:
            user = session.query(User).filter(User.login == login).first()
            if user:
                flash('User with the same login already exists')
                return render_template(edit_page, groups=groups, form_caption=form_caption, submit_text=submit_text)

            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                abort(404)

            user.login = login
            user.access_group = access_group
            session.commit()

        return redirect(url_for('users.index'))

    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404)

    return render_template(edit_page, groups=groups, form_caption=form_caption, user=user, submit_text=submit_text)


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
