from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import AccessGroup, User
from organizer.strings import STRING_TABLE


def test_non_logged_user_can_see(client: FlaskClient):
    response = client.get('/auth/signup')
    assert 200 == response.status_code
    assert b'<title>' in response.data


def test_logged_user_is_redirected(org_logged_client: FlaskClient):
    response = org_logged_client.get('/auth/signup')
    assert 302 == response.status_code
    assert '/trips/' in response.location


def test_can_create_user(client: FlaskClient):
    response = client.post('/api/auth/signup/', json={
        'login': 'test@test.com',
        'password': 'long-password'
    })
    assert 201 == response.status_code

    with client.application.app_context():
        with get_session() as session:
            session.query(User).filter(User.login == 'test@test.com',
                                       User.access_group == AccessGroup.User).one()


@pytest.mark.parametrize('json', [
    {'login': 'non-email', 'password': 'long-password'},
    {'login': 'email@no-top-level-domain', 'password': 'long-password'},
    {'login': '', 'password': 'long-password'},
    {'login': 'correct@email.com', 'password': 'short'},
    {'login': 'correct@email.com', 'password': ''},
    {'login': 'a'*50 + '@email.com', 'password': 'long-password'},
    {'login': 'test@test.com'},
    {'password': 'long-password'},
])
def test_cannot_create_user_with_incorrect_data(client: FlaskClient, json: dict):
    response = client.post('/api/auth/signup/', json=json)
    assert 400 == response.status_code


def test_cannot_create_user_with_incorrect_request(client: FlaskClient):
    response = client.post('/api/auth/signup/')
    assert 415 == response.status_code


def test_cannon_create_user_with_the_same_login(client: FlaskClient):
    response = client.post('/api/auth/signup/', json={
        'login': 'test@test.com',
        'password': '12345678'
    })
    assert 201 == response.status_code

    response = client.post('/api/auth/signup/', json={
        'login': 'test@test.com',
        'password': '12345678'
    })
    assert 422 == response.status_code
    assert STRING_TABLE['Signup user already exists'] in response.json['message']
