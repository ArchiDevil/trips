from bs4 import BeautifulSoup

from flask.testing import FlaskClient

# TODO: no tests check correctness of the data
from organizer.strings import STRING_TABLE


def test_shopping_returns_404_on_invalid_trip_id(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/shopping/uid100')
    assert response.status_code == 404


def test_packing_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/reports/packing/uid1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_packing_redirects_to_columns_report(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/packing/uid1')
    assert response.status_code == 302
    assert '/reports/packing/uid1/4' in response.location


def test_packing_custom_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/reports/packing/1/4')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_packing_custom_shows_non_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/packing/uid3/1')
    assert response.status_code == 200


def test_packing_custom_shows_report(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/packing/uid1/4')
    assert response.status_code == 200
    assert b'Taganay' in response.data
    assert b'Mango' in response.data
    assert ('2 ' + STRING_TABLE['Packing report persons suffix']).encode() in response.data
    assert ('3 ' + STRING_TABLE['Packing report persons suffix']).encode() in response.data


def test_packing_custom_returns_404_on_invalid_trip_id(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/packing/uid100/4')
    assert response.status_code == 404


def test_packing_custom_returns_403_on_invalid_columns_count(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/packing/uid1/7')
    assert response.status_code == 403
    response = org_logged_client.get('/reports/packing/uid1/0')
    assert response.status_code == 403


def test_packing_custom_does_not_show_empty_day(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/packing/uid1/4')
    assert (STRING_TABLE['Packing report day title'] + ' 4').encode() not in response.data


def test_packing_custom_has_correct_days_order(org_logged_client: FlaskClient):
    response = org_logged_client.get('/reports/packing/uid1/4')
    data = response.data.decode(encoding='utf-8')
    assert data

    idx = 0
    soup = BeautifulSoup(data, 'html.parser')
    assert soup.body
    for child in soup.body.find_all('table'):
        rows = child.find_all('tr')
        assert (idx == 0 and len(rows) == 14) or (idx != 0 and len(rows) == 8)
        idx += 1
