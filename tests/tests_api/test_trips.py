from flask.testing import FlaskClient

from organizer.db import get_session
from organizer.schema import TripAccess


def test_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/api/trips/get')
    assert response.status_code == 403


def test_can_get_trips_for_guest(user_logged_client: FlaskClient):
    response = user_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert not response.json['trips']


def test_can_get_trips_for_manager(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert len(response.json['trips']) == 1


def test_can_get_shared_trips(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            # add admin trip to org
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert len(response.json['trips']) == 2


def test_trips_can_share(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get')
    assert response.json
    assert 1 == len(response.json['trips'])

    org_logged_client.get('/meals/3')
    response = org_logged_client.get('/api/trips/get')
    assert response.json
    assert 2 == len(response.json['trips'])


def test_trips_returns_correct_data_for_admin(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert 2 == len(response.json['trips'])


def test_trips_guest_cannon_access_trips(client: FlaskClient):
    response = client.get('/api/trips/get/1')
    assert response.status_code == 403


def test_trips_user_cannot_access_trips(user_logged_client: FlaskClient):
    response = user_logged_client.get('/api/trips/get/1')
    assert response.status_code == 403


def test_trips_org_can_get_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get/1')
    assert response.status_code == 200
    assert response.json
    assert response.json['trip']
    assert response.json['id'] == 1


def test_trips_org_cannot_access_non_owned_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get/3')
    assert response.status_code == 403


def test_trips_org_can_access_shared_trip(org_logged_client: FlaskClient):
    org_logged_client.get('/meals/3')

    response = org_logged_client.get('/api/trips/get/3')
    assert response.status_code == 200
    assert response.json
    assert response.json['trip']
    assert response.json['id'] == 3


def test_trips_admin_can_access_all_trips(admin_logged_client: FlaskClient):
    for trip_id in range(3):
        response = admin_logged_client.get(f'/api/trips/get/{trip_id + 1}')
        assert response.status_code == 200
        assert response.json
        assert response.json['trip']
        assert response.json['id'] == trip_id + 1


def test_trips_cannot_access_non_existing_trip(user_logged_client: FlaskClient):
    response = user_logged_client.get('/api/trips/get/100500')
    assert response.status_code == 404
