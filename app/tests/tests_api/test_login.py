from flask import Flask
from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import User
from organizer.strings import STRING_TABLE


def test_auth_can_log_in_as_user(client: FlaskClient):
    response = client.post('/api/auth/login/',
                           json={
                               'login': 'Administrator',
                               'password': 'qwerty'
                           })
    assert client.get_cookie('session')
    assert not client.get_cookie('session').expires

    assert response.status_code == 200
    assert response.json
    assert 'message' in response.json


def test_auth_updates_last_login(client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            user = session.query(User).filter(User.login == "Administrator").one()
            first_date = user.last_logged_in

    client.post('/api/auth/login/',
                json={
                    'login': 'Administrator',
                    'password': 'qwerty'
                })

    with app.app_context():
        with get_session() as session:
            user = session.query(User).filter(User.login == "Administrator").one()
            second_date = user.last_logged_in

    assert first_date != second_date


def test_auth_can_log_in_as_user_with_remember(client: FlaskClient):
    response = client.post('/api/auth/login/',
                           json={
                               'login': 'Administrator',
                               'password': 'qwerty',
                               'remember': 'true'
                           })
    assert client.get_cookie('session')
    assert client.get_cookie('session').expires

    assert response.status_code == 200
    assert response.json
    assert 'message' in response.json


@pytest.mark.parametrize('credentials', [
    {'login': 'No no no', 'password': 'qwerty'},
    {'login': 'Administrator', 'password': 'invalid pass'}
])
def test_auth_reports_invalid_creds(client: FlaskClient, credentials):
    response = client.post('/api/auth/login/',
                           json=credentials)
    assert response.status_code == 422
    assert response.json
    assert 'message' in response.json
    assert STRING_TABLE['Login errors invalid creds'] == response.json['message']
