import functools
from datetime import datetime, timedelta
from urllib.parse import urlencode
from typing import Optional
import requests

from flask import Blueprint, render_template, request, g, redirect, url_for, \
                  session, flash, abort, current_app

from sentry_sdk import configure_scope, capture_exception

from organizer.db import get_session
from organizer.schema import PasswordLink, User, AccessGroup, VkUser, UserType
from organizer.strings import STRING_TABLE

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required_group(group):
    def login_required_grouped(view):
        @functools.wraps(view)
        def wrapped_view_grouped(**kwargs):
            if 'user' not in g or g.user is None:
                return redirect(url_for('auth.index', path='login', redirect=request.path))
            if g.user.access_group.value < group.value:
                abort(403)
            with configure_scope() as scope:
                name: str = g.user.displayed_name if g.user.displayed_name else g.user.login
                scope.user = {
                    'id': str(g.user.id),
                    'username': f'{name}'
                }

            # update last user login/access
            with get_session() as sql_session:
                user = sql_session.query(User).filter(User.id == g.user.id).first()
                user.last_logged_in = datetime.utcnow()
                sql_session.commit()

            return view(**kwargs)
        return wrapped_view_grouped
    return login_required_grouped


def api_login_required_group(group=None):
    def api_login_required_grouped(view):
        @functools.wraps(view)
        def api_wrapped_view_grouped(**kwargs):
            if 'user' not in g or g.user is None:
                abort(403)
            if group and g.user.access_group.value < group.value:
                abort(403)
            return view(**kwargs)
        return api_wrapped_view_grouped
    return api_login_required_grouped


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        with get_session() as sql_session:
            result = sql_session.query(User.user_type).filter(User.id == user_id).one()
            if result.user_type == UserType.Vk:
                result = sql_session.query(User.id, User.access_group,
                                           User.displayed_name, User.login,
                                           User.user_type, VkUser.photo_url).filter(User.id == user_id,
                                                                                    VkUser.user_id == user_id).one()
            else:
                result = sql_session.query(User.id, User.access_group,
                                           User.displayed_name, User.login,
                                           User.user_type).filter(User.id == user_id).one()
            g.user = result


@bp.get('/', defaults={'path': ''})
@bp.get('/<path:path>')
def index(path):
    redirect_location = request.args['redirect'] if 'redirect' in request.args else url_for('trips.index')

    if 'user' in g and g.user is not None:
        return redirect(redirect_location)

    return render_template('auth/auth.html', redirect=redirect_location)


@bp.get('/reset/<uuid:token>')
def reset(token):
    if 'user' in g and g.user is not None:
        return redirect(url_for('trips.index'))

    with get_session() as session:
        link: Optional[PasswordLink] = session.query(PasswordLink).filter(PasswordLink.uuid == str(token)).first()
        if not link:
            abort(404)

        if link.expiration_date < datetime.utcnow():
            abort(404)

    return render_template('auth/reset.html', token=str(token))


@bp.get('/logout')
@login_required_group(AccessGroup.User)
def logout():
    with configure_scope() as scope:
        scope.user = None
    session.clear()
    return redirect(url_for('trips.index'))


@bp.get('/vk_login')
def vk_login():
    url = 'https://oauth.vk.com/authorize?'
    query = urlencode({
        'client_id': current_app.config['VK_CLIENT_ID'],
        'redirect_uri': url_for('auth.vk_redirect', _external=True),
        'state': request.args['redirect']
    })
    return redirect(url + query)


def create_vk_user(sql_session, login, user_id, displayed_name, access_token, expires_in, photo_url):
    new_user = User(login=login,
                    displayed_name=displayed_name,
                    access_group=AccessGroup.User,
                    user_type=UserType.Vk)
    sql_session.add(new_user)
    sql_session.commit()

    added_user = sql_session.query(User).filter(User.login == login).one()
    vk_user = VkUser(id=user_id,
                     user_id=added_user.id,
                     user_token=access_token,
                     token_exp_time= datetime.utcnow() + timedelta(seconds=expires_in),
                     photo_url=photo_url)
    sql_session.add(vk_user)
    sql_session.commit()
    return added_user.id


def login_as_vk_user(login, access_token, vk_user_id, displayed_name, expires_in, photo_url):
    with get_session() as sql_session:
        native_user = sql_session.query(User).filter(User.login == login).first()
        if not native_user:
            native_user_id = create_vk_user(sql_session, login,
                                            vk_user_id, displayed_name,
                                            access_token, expires_in,
                                            photo_url)
        else:
            assert native_user.user_type == UserType.Vk
            native_user_id = native_user.id
            vk_user = sql_session.query(VkUser).filter(VkUser.id == vk_user_id,
                                                       VkUser.user_id == native_user.id).one()
            vk_user.user_token = access_token
            vk_user.token_exp_time = datetime.utcnow() + timedelta(seconds=expires_in)
            vk_user.photo_url = photo_url
            sql_session.commit()

        session.clear()
        session['user_id'] = native_user_id


def request_vk_access_token(code):
    result = requests.get('https://oauth.vk.com/access_token',
                          params={
                              'client_id': current_app.config['VK_CLIENT_ID'],
                              'client_secret': current_app.config['VK_APP_SECRET'],
                              'redirect_uri': url_for('auth.vk_redirect', _external=True),
                              'code': code
                          })

    json_result = result.json()
    if 'error' in json_result:
        raise RuntimeError('Error from vk server [{}]: {}'.format(json_result['error'],
                                                                  json_result['error_description']))

    return json_result['access_token'], json_result['expires_in'], json_result['user_id']


def request_vk_user_name_and_photo(access_token):
    result = requests.get('https://api.vk.com/method/users.get',
                          params={
                              'fields': 'photo_50',
                              'access_token': access_token,
                              'v': '5.103'
                          })

    json_result = result.json()
    if 'error' in json_result:
        raise RuntimeError('Error from vk server [{}]: {}'.format(json_result['error'],
                                                                  json_result['error_description']))

    response_user = json_result['response'][0]
    return f'{response_user["first_name"]} {response_user["last_name"]}', response_user['photo_50']


@bp.get('/vk_redirect')
def vk_redirect():
    code = request.args['code']
    redirect_location = request.args['state']

    try:
        access_token, expires_in, vk_user_id = request_vk_access_token(code)
        displayed_name, photo_url = request_vk_user_name_and_photo(access_token)
    except RuntimeError as exc:
        capture_exception(exc)
        flash(STRING_TABLE['Login errors vk error'])
        return redirect(url_for('.login'))

    login = f'vk_{vk_user_id}'
    login_as_vk_user(login, access_token, vk_user_id,
                     displayed_name, expires_in, photo_url)

    return redirect(redirect_location)
