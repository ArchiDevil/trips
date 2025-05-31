from uuid import uuid4
from datetime import datetime, timedelta

from flask import Flask
from flask.testing import FlaskClient

from organizer.db import get_session
from organizer.schema import User, PasswordLink


def test_auth_can_see_login_page(client: FlaskClient):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert 'Hikehub' in response.data.decode('utf-8')


def test_auth_any_access_updates_last_login(admin_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            user = session.query(User).where(User.login == "Administrator").one()
            first_date = user.last_logged_in

    response = admin_logged_client.get('/api/trips/')
    assert response.status_code == 200

    with app.app_context():
        with get_session() as session:
            user = session.query(User).where(User.login == "Administrator").one()
            second_date = user.last_logged_in

    assert first_date != second_date


def test_auth_logout_requires_login(client: FlaskClient):
    response = client.get('/auth/logout')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_auth_can_logout(org_logged_client: FlaskClient):
    response = org_logged_client.get('/auth/logout')
    assert not org_logged_client.get_cookie('session')
    assert response.status_code == 302
    assert '/' in response.location


def test_forgot_shows_page(client: FlaskClient):
    response = client.get('/auth/forgot')
    assert response.status_code == 200


def test_forgot_show_redirect_logged_in(org_logged_client: FlaskClient):
    response = org_logged_client.get('/auth/forgot')
    assert response.status_code == 302
    assert '/trips' in response.location


def test_reset_shows_page(client: FlaskClient):
    uuid = str(uuid4())
    with client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(user_id=1, uuid=uuid))
            session.commit()

    response = client.get(f'/auth/reset/{uuid}')
    assert response.status_code == 200


def test_reset_rejects_invalid_token(client: FlaskClient):
    response = client.get(f'/auth/reset/{uuid4()}')
    assert response.status_code == 404


def test_reset_rejects_old_link(client: FlaskClient):
    uuid = str(uuid4())
    with client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(uuid=uuid, user_id=1, expiration_date=(datetime.utcnow() - timedelta(days=10))))
            session.commit()

    response = client.get(f'/auth/reset/{uuid}')
    assert response.status_code == 404


def test_reset_redirects_logged_in(org_logged_client: FlaskClient):
    uuid = str(uuid4())
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(user_id=1, uuid=uuid))
            session.commit()

    response = org_logged_client.get(f'/auth/reset/{uuid}')
    assert response.status_code == 302
    assert '/trips/' in response.location
