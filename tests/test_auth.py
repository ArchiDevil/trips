from flask import Flask

from organizer.strings import STRING_TABLE
from organizer.db import get_session
from organizer.schema import User

def test_auth_can_see_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert STRING_TABLE['Login title'].encode() in response.data


def test_auth_can_log_in_as_user(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'Administrator',
                               'password': 'qwerty',
                               'redirect': '/trip/edit/1'
                           })
    assert client.cookie_jar
    for x in client.cookie_jar:
        assert not x.expires

    assert response.status_code == 302
    assert '/trip/edit/1' in response.location


def test_auth_updates_last_login(client, app: Flask):
    with app.app_context():
        with get_session() as session:
            user = session.query(User).filter(User.login == "Administrator").first()
            first_date = user.last_logged_in

    client.post('/auth/login',
                data={
                    'login': 'Administrator',
                    'password': 'qwerty',
                    'redirect': '/trip/edit/1'
                })

    with app.app_context():
        with get_session() as session:
            user = session.query(User).filter(User.login == "Administrator").first()
            second_date = user.last_logged_in

    assert first_date != second_date


def test_auth_any_access_updates_last_login(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            user = session.query(User).filter(User.login == "Organizer").first()
            first_date = user.last_logged_in

    response = org_logged_client.get('/meals/1')
    assert response.status_code == 200

    with app.app_context():
        with get_session() as session:
            user = session.query(User).filter(User.login == "Organizer").first()
            second_date = user.last_logged_in

    assert first_date != second_date


def test_auth_can_log_in_as_user_with_remember(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'Administrator',
                               'password': 'qwerty',
                               'remember': 'true',
                               'redirect': '/trip/edit/1'
                           })
    assert client.cookie_jar
    for x in client.cookie_jar:
        assert x.expires

    assert response.status_code == 302
    assert '/trip/edit/1' in response.location


def test_auth_reports_login_error(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'No no no',
                               'password': 'qwerty',
                               'redirect': '/trip/edit/1'
                           })
    assert response.status_code == 200
    assert STRING_TABLE['Login errors no user'].encode('utf-8') in response.data


def test_auth_reports_password_error(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'Administrator',
                               'password': 'invalid pass',
                               'redirect': '/trip/edit/1'
                           })
    assert response.status_code == 200
    assert STRING_TABLE['Login errors incorrect password'].encode('utf-8') in response.data


def test_auth_redirects_without_field(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'Administrator',
                               'password': 'qwerty'
                           })
    assert response.status_code == 302
    assert '/trips/' in response.location


def test_auth_logout_requires_login(client):
    response = client.get('/auth/logout')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_auth_can_logout(org_logged_client):
    response = org_logged_client.get('/auth/logout')
    assert not org_logged_client.cookie_jar
    assert response.status_code == 302
    assert '/' in response.location
