from flask.testing import FlaskClient

from organizer.strings import STRING_TABLE

def test_info_page_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/info/')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_info_page_is_shown(org_logged_client: FlaskClient):
    response = org_logged_client.get('/info/')
    assert response.status_code == 200
    assert STRING_TABLE['Info title'].encode() in response.data
