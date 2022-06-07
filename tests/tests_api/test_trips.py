from datetime import datetime, timedelta
from itertools import product

from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import TripAccess, SharingLink, TripAccessType


def test_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/api/trips/get')
    assert response.status_code == 403


def test_can_get_trips_for_manager(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert len(response.json['trips']) == 1


def test_can_get_shared_trips(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2, access_type=TripAccessType.Read))
            session.commit()

    response = org_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert len(response.json['trips']) == 2


def test_trips_returns_correct_data_for_admin(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/api/trips/get')
    assert response.status_code == 200
    assert response.json
    assert 2 == len(response.json['trips'])


def test_trips_guest_cannon_access_trips(client: FlaskClient):
    response = client.get('/api/trips/get/1')
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
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2, access_type=TripAccessType.Read))
            session.commit()

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


def test_trips_cannot_access_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get/100500')
    assert response.status_code == 404


def test_trips_shared_rejects_non_logged_user(client: FlaskClient):
    response = client.get('/api/trips/share/1/read')
    assert response.status_code == 403


@pytest.mark.parametrize('access_type', ['read', 'write'])
def test_trips_share_generates_response(org_logged_client: FlaskClient, access_type: str):
    response = org_logged_client.get(f'/api/trips/share/1/{access_type}')
    assert response.status_code == 200

    assert response.json
    json = response.json

    assert json['uuid']
    uuid = json['uuid']

    assert json['link']
    assert f'/access/{uuid}' in json['link']


@pytest.mark.parametrize('access_type, trip_id', product(['read', 'write'], range(1, 4)))
def test_trips_share_admin_can_share_any_trip(admin_logged_client: FlaskClient, access_type: str, trip_id: int):
    response = admin_logged_client.get(f'/api/trips/share/{trip_id}/{access_type}')
    assert response.status_code == 200

    assert response.json
    json = response.json

    assert json['uuid']
    uuid = json['uuid']

    assert json['link']
    assert f'/access/{uuid}' in json['link']


def test_trips_share_stores_link_info(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/1/read')
    assert response.status_code == 200
    assert response.json
    uuid1 = response.json['uuid']

    response = org_logged_client.get('/api/trips/share/1/write')
    assert response.status_code == 200
    assert response.json
    uuid2 = response.json['uuid']

    with org_logged_client.application.app_context():
        with get_session() as session:
            link1: SharingLink = session.query(SharingLink).filter(SharingLink.uuid == uuid1).one()
            assert link1.access_type == TripAccessType.Read
            assert link1.uuid == uuid1
            assert link1.expiration_date.day == (datetime.utcnow() + timedelta(days=3)).day

            link2: SharingLink = session.query(SharingLink).filter(SharingLink.uuid == uuid2).one()
            assert link2.access_type == TripAccessType.Write
            assert link2.uuid == uuid2
            assert link2.expiration_date.day == (datetime.utcnow() + timedelta(days=3)).day


@pytest.mark.parametrize('type_', ['read', 'write'])
def test_trips_share_does_not_duplicate_link(org_logged_client: FlaskClient, type_: str):
    response = org_logged_client.get(f'/api/trips/share/1/{type_}')
    assert response.status_code == 200
    assert response.json
    uuid1 = response.json['uuid']
    link1 = response.json['link']

    response = org_logged_client.get(f'/api/trips/share/1/{type_}')
    assert response.status_code == 200
    assert response.json
    uuid2 = response.json['uuid']
    link2 = response.json['link']

    assert uuid1 == uuid2
    assert link1 == link2


@pytest.mark.parametrize('type_', ['read', 'write'])
def test_trips_share_updates_expiration_time(org_logged_client: FlaskClient, type_: str):
    response = org_logged_client.get(f'/api/trips/share/1/{type_}')
    assert response.status_code == 200
    assert response.json

    with org_logged_client.application.app_context():
        with get_session() as session:
            link: SharingLink = session.query(SharingLink).filter(SharingLink.uuid == response.json['uuid']).one()
            first_time = link.expiration_date

    response = org_logged_client.get(f'/api/trips/share/1/{type_}')
    assert response.status_code == 200
    assert response.json

    with org_logged_client.application.app_context():
        with get_session() as session:
            link: SharingLink = session.query(SharingLink).filter(SharingLink.uuid == response.json['uuid']).one()
            assert first_time != link.expiration_date


def test_trips_share_rejects_incorrect_sharing_type(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/1/incorrect')
    assert response.status_code == 400


def test_trips_share_rejects_non_accessed_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/3/read')
    assert response.status_code == 403


def test_trips_share_rejects_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/100500/read')
    assert response.status_code == 404
