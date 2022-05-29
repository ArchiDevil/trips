from flask.testing import FlaskClient

from organizer.schema import Trip
from organizer.db import get_session
from organizer.strings import STRING_TABLE


def test_trips_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_shows_trips_page(user_logged_client: FlaskClient):
    response = user_logged_client.get('/trips/')
    assert response.status_code == 200


def test_trips_archive_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/archive/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_archive_rejects_guest(user_logged_client: FlaskClient):
    response = user_logged_client.get('/trips/archive/1')
    assert response.status_code == 403


def test_trips_can_archive(org_logged_client: FlaskClient, app):
    response = org_logged_client.get('/trips/archive/1')
    assert response.status_code == 302
    assert '/' in response.location

    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip.id, Trip.archived).filter(Trip.id == 1).one()
            assert trip.archived


def test_trips_archive_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/archive/100')
    assert response.status_code == 404


def test_trips_forget_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/forget/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_forget_returns_404_for_non_existing_trip(user_logged_client: FlaskClient):
    response = user_logged_client.get('/trips/forget/100')
    assert response.status_code == 404


def test_trips_forget_forgets_trip(user_logged_client: FlaskClient):
    user_logged_client.get('/meals/1')
    response = user_logged_client.get('/trips/forget/1')
    assert response.status_code == 302
    assert '/' in response.location

    response = user_logged_client.get('/api/trips/get')
    assert response.json
    assert 0 == len(response.json['trips'])


def test_trips_forgetting_unknown_does_nothing(user_logged_client: FlaskClient):
    response = user_logged_client.get('/trips/forget/3')
    assert response.status_code == 302
    assert response.location.endswith('/')


def test_trips_download_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/download/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_download_returns_csv(user_logged_client: FlaskClient):
    response = user_logged_client.get('/trips/download/1')
    assert response.status_code == 200
    assert response.data

    # BOM
    assert response.data[0] == 0xEF
    assert response.data[1] == 0xBB
    assert response.data[2] == 0xBF

    data: str = response.data[3:].decode(encoding='utf-8')
    lines = data.splitlines()
    assert lines
    assert len(lines) == 39
    assert lines[0] == ','.join([
        STRING_TABLE['CSV name'],
        STRING_TABLE['CSV day'],
        STRING_TABLE['CSV meal'],
        STRING_TABLE['CSV mass'],
        STRING_TABLE['CSV cals']
    ])
    assert ','.join([
        'Multigrain cereal', '3', STRING_TABLE['Meals breakfast title'], '60', '362.0'
    ]) in lines


def test_trips_download_returns_empty_csv(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/trips/download/3')
    assert response.status_code == 200
    assert response.data

    # skip BOM
    data: str = response.data[3:].decode(encoding='utf-8')
    lines = data.splitlines()
    assert lines
    assert len(lines) == 1
    assert lines[0] == ','.join([
        STRING_TABLE['CSV name'],
        STRING_TABLE['CSV day'],
        STRING_TABLE['CSV meal'],
        STRING_TABLE['CSV mass'],
        STRING_TABLE['CSV cals']
    ])


def test_trips_download_returns_404_for_non_existing_trip(user_logged_client: FlaskClient):
    response = user_logged_client.get('/trips/download/42')
    assert response.status_code == 404
