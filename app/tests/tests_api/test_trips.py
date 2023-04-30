from datetime import datetime, timedelta

from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import SharingLink, TripAccess


def test_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/api/trips/get')
    assert response.status_code == 403


def test_can_get_trips_for_manager(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert len(response.json['trips']) == 1
    assert response.json['trips'][0] == 'uid1'


def test_can_get_shared_trip_uids(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert len(response.json['trips']) == 2
    assert response.json['trips'][0] == 'uid1'
    assert response.json['trips'][1] == 'uid3'


def test_trips_returns_correct_data_for_admin(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert 2 == len(response.json['trips'])


def test_trips_guest_cannot_access_trips(client: FlaskClient):
    response = client.get('/api/trips/get/uid1')
    assert response.status_code == 403


def test_trips_org_can_get_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get/uid1')
    assert response.status_code == 200
    assert response.json
    assert response.json['trip']
    assert response.json['uid'] == 'uid1'


def test_trips_org_can_access_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get/uid3')
    assert response.status_code == 200
    assert response.json
    assert response.json['trip']
    assert response.json['uid'] == 'uid3'


def test_trips_admin_can_access_all_trips(admin_logged_client: FlaskClient):
    for trip_id in range(3):
        response = admin_logged_client.get(f'/api/trips/get/uid{trip_id + 1}')
        assert response.status_code == 200
        assert response.json
        assert response.json['trip']
        assert response.json['uid'] == f'uid{trip_id + 1}'


def test_trips_cannot_access_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get/100500')
    assert response.status_code == 404


def test_trips_share_rejects_non_logged_user(client: FlaskClient):
    response = client.get('/api/trips/share/uid1')
    assert response.status_code == 403


def test_trips_share_generates_response(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200

    assert response.json
    json = response.json

    assert json['uuid']
    uuid = json['uuid']

    assert json['link']
    assert f'/access/{uuid}' in json['link']


@pytest.mark.parametrize('trip_id', [1, 2, 3])
def test_trips_share_admin_can_share_any_trip(admin_logged_client: FlaskClient, trip_id: int):
    response = admin_logged_client.get(f'/api/trips/share/uid{trip_id}')
    assert response.status_code == 200

    assert response.json
    json = response.json

    assert json['uuid']
    uuid = json['uuid']

    assert json['link']
    assert f'/access/{uuid}' in json['link']


def test_trips_share_stores_link_info(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200
    assert response.json
    uuid = response.json['uuid']

    with org_logged_client.application.app_context():
        with get_session() as session:
            link2: SharingLink = session.query(SharingLink).one()
            assert link2.uuid == uuid
            assert link2.expiration_date.day == (datetime.utcnow() + timedelta(days=3)).day


def test_trips_share_does_not_duplicate_link(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200
    assert response.json
    uuid1 = response.json['uuid']
    link1 = response.json['link']

    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200
    assert response.json
    uuid2 = response.json['uuid']
    link2 = response.json['link']

    assert uuid1 == uuid2
    assert link1 == link2


def test_trips_share_updates_expiration_time(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200
    assert response.json

    with org_logged_client.application.app_context():
        with get_session() as session:
            link: SharingLink = session.query(SharingLink).filter(SharingLink.uuid == response.json['uuid']).one()
            first_time = link.expiration_date

    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200
    assert response.json

    with org_logged_client.application.app_context():
        with get_session() as session:
            link: SharingLink = session.query(SharingLink).filter(SharingLink.uuid == response.json['uuid']).one()
            assert first_time != link.expiration_date


def test_trips_share_rejects_non_accessed_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid3')
    assert response.status_code == 403


def test_trips_share_rejects_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid100500')
    assert response.status_code == 404
