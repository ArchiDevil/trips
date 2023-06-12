import re
import json
from datetime import datetime
from uuid import uuid4
from typing import Optional, Final

from flask import Blueprint, current_app, g, render_template, request, \
                  abort, url_for, session
from flask.wrappers import Response

from werkzeug.security import check_password_hash, generate_password_hash

from organizer.auth import api_login_required_group
from organizer.db import create_user, get_session
from organizer.schema import AccessGroup, PasswordLink, User
from organizer.strings import STRING_TABLE
from organizer.utils.auth import is_captcha_enabled, check_captcha
from organizer.utils.email import send_email

BP = Blueprint('auth', __name__, url_prefix='/auth')


@BP.get('/user')
@api_login_required_group(AccessGroup.User)
def user():
    return {
        'id': g.user.id,
        'login': g.user.login,
        'displayed_name': g.user.displayed_name,
        'access_group': g.user.access_group.name,
        'user_type': g.user.user_type.name,
        'photo_url': g.user.photo_url if 'photo_url' in g.user.keys() else None
    }


@BP.post('/login/')
def login():
    user_login = request.json['login']
    user_password = request.json['password']
    remember_login = 'remember' in request.json.keys()

    if is_captcha_enabled():
        recaptcha_response = request.json['g-recaptcha-response']
        if not check_captcha(recaptcha_response):
            return Response(
                json.dumps({'message': STRING_TABLE['Login errors recaptcha']}),
                status=422, mimetype='application/json')

    with get_session() as sql_session:
        user = sql_session.query(User).filter(User.login == user_login).first()
        if not user or not check_password_hash(user.password, user_password) or not user.password:
            return Response(
                json.dumps({'message': STRING_TABLE['Login errors invalid creds']}),
                status=422, mimetype='application/json')
        else: # no issues
            user.last_logged_in = datetime.utcnow()
            sql_session.commit()

            session.clear()
            session['user_id'] = user.id
            session.permanent = remember_login
            return {
                'message': STRING_TABLE['Login success'],
            }


@BP.post('/signup/')
def signup():
    login: str = request.json.get('login', '')
    password: str = request.json.get('password', '')

    if not login or not password:
        abort(400)

    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", login):
        abort(400)

    if len(password) < 8 or len(login) > 50:
        abort(400)

    if is_captcha_enabled():
        recaptcha_response = request.json['g-recaptcha-response']
        if not check_captcha(recaptcha_response):
            abort(400)

    try:
        create_user(login, password, AccessGroup.User)
    except ValueError:
        return Response(
            json.dumps({'message': STRING_TABLE['Signup user already exists']}),
            status=422, mimetype='application/json')

    return Response(json.dumps({'message': STRING_TABLE['Signup successful']}),
                    status=201)


@BP.post('/forgot/')
def forgot():
    if 'user' in g and g.user is not None:
        abort(403)

    if is_captcha_enabled():
        captcha_response = request.json['g-recaptcha-response']
        if not check_captcha(captcha_response):
            data = json.dumps({
                'message': STRING_TABLE['Login errors recaptcha']
            })
            return Response(data, status=422, content_type='application/json')

    form_login = request.json['login']
    with get_session() as session:
        user = session.query(User).filter(User.login == form_login).first()
        if not user:
            data = json.dumps({
                'message': STRING_TABLE['Forgot invalid login']
            })
            return Response(data, status=422, content_type='application/json')

        uuid = str(uuid4())
        session.add(PasswordLink(uuid=uuid,
                                 user_id=user.id))
        session.commit()

    # send a link via send-in-blue
    if 'SENDINBLUE_APP_KEY' in current_app.config:
        reset_link = url_for('auth.reset', token=uuid, _external=True, _scheme='https')
        email_body = render_template('reset_password_email.html', sitename=current_app.config['SERVER_NAME'], reset_link=reset_link)
        try:
            send_email(form_login,
                    STRING_TABLE['Forgot email subject'],
                    email_body)
        except RuntimeError:
            data = json.dumps({
                'message': STRING_TABLE['Forgot email error']
            })
            return Response(data, status=422, content_type='application/json')

    return {
        'message': STRING_TABLE['Forgot ok']
    }


@BP.post('/reset/')
def reset():
    token = request.json.get('token', '')
    password = request.json.get('password', '')
    current_time: Final = datetime.utcnow()

    if len(password) < 8:
        abort(400)

    with get_session() as session:
        session.query(PasswordLink).filter(PasswordLink.expiration_date < current_time).delete()
        session.commit()

        link: Optional[PasswordLink] = session.query(PasswordLink).filter(PasswordLink.uuid == token).first()
        if not link:
            abort(400)

        session.delete(link)
        session.commit()

        user: User = session.query(User).filter(User.id == link.user_id).one()
        user.password = generate_password_hash(password)
        session.commit()

    return Response({}, status=200)
