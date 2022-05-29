from flask.testing import FlaskClient

from organizer.schema import AccessGroup, UserType


def test_user_api_returns_403_for_non_logged_in_user(client: FlaskClient):
    response = client.get('/api/auth/user')
    assert response.status_code == 403


def test_can_get_user_info(user_logged_client: FlaskClient):
    response = user_logged_client.get('/api/auth/user')
    assert response.status_code == 200
    assert response.json
    assert response.json['id']
    assert 'User' == response.json['login']
    assert AccessGroup.Guest.name == response.json['access_group']
    assert UserType.Native.name == response.json['user_type']
