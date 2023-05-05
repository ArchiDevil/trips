from flask.testing import FlaskClient

from organizer.schema import AccessGroup, UserType


def test_user_api_returns_unauthorized_for_non_logged_in_user(client: FlaskClient):
    response = client.get('/api/auth/user')
    assert response.status_code == 401


def test_can_get_user_info(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/auth/user')
    assert response.status_code == 200
    assert response.json
    assert response.json['id']
    assert 'Organizer' == response.json['login']
    assert AccessGroup.User.name == response.json['access_group']
    assert UserType.Native.name == response.json['user_type']
