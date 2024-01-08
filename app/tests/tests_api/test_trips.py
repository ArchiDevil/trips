from datetime import datetime, timedelta
from typing import Any

from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import SharingLink, Trip, TripAccess


def test_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/api/trips/get')
    assert response.status_code == 401


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
    assert response.status_code == 401


def test_trips_org_can_get_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/get/uid1')
    assert response.status_code == 200
    assert response.json
    assert response.json['trip']
    assert response.json['uid'] == 'uid1'
    assert response.json['type'] == 'user'
    assert response.json['attendees'] == 5
    assert response.json['cover_src'] == '/static/img/trips/7.png'
    assert response.json['open_link'] == '/meals/uid1'
    assert response.json['edit_link'] == '/trips/edit/uid1'
    assert response.json['forget_link'] == '/trips/forget/uid1'
    assert response.json['packing_link'] == '/reports/packing/uid1'
    assert response.json['shopping_link'] == '/reports/shopping/uid1'
    assert response.json['download_link'] == '/trips/download/uid1'

    assert response.json['trip']['name'] == 'Taganay trip'
    assert response.json['trip']['from_date'] == '2019-01-01'
    assert response.json['trip']['till_date'] == '2019-01-05'
    assert response.json['trip']['days_count'] == 5
    assert response.json['trip']['created_by'] == 2
    assert response.json['trip']['archived'] is False
    assert response.json['trip']['groups'] == [2, 3]
    assert response.json['trip']['user'] == 'Organizer'
    assert response.json['trip']['share_link'] == '/api/trips/share/uid1'
    assert response.json['trip']['archive_link'] == '/api/trips/archive/uid1'


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
    assert response.status_code == 401


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
def test_trips_share_admin_can_share_any_trip(
    admin_logged_client: FlaskClient, trip_id: int
):
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
            assert (
                link2.expiration_date.day == (datetime.utcnow() + timedelta(days=3)).day
            )


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
            link: SharingLink = (
                session.query(SharingLink)
                .filter(SharingLink.uuid == response.json['uuid'])
                .one()
            )
            first_time = link.expiration_date

    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200
    assert response.json

    with org_logged_client.application.app_context():
        with get_session() as session:
            link: SharingLink = (
                session.query(SharingLink)
                .filter(SharingLink.uuid == response.json['uuid'])
                .one()
            )
            assert first_time != link.expiration_date


def test_trips_share_rejects_non_accessed_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid3')
    assert response.status_code == 403


def test_trips_share_rejects_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/share/uid100500')
    assert response.status_code == 404


def test_trips_can_archive(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/archive/uid1')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.uid == 'uid1').one()
            assert trip.archived


def test_trips_archive_returns_404_for_non_existing_trip(
    org_logged_client: FlaskClient,
):
    response = org_logged_client.post('/api/trips/archive/uid100500')
    assert response.status_code == 404


def test_trips_archive_rejects_non_accessed_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/archive/uid3')
    assert response.status_code == 403


def test_trips_archive_rejects_non_logged_user(client: FlaskClient):
    response = client.post('/api/trips/archive/uid1')
    assert response.status_code == 401


def test_trips_add_rejects_not_logged_in(client: FlaskClient):
    response = client.post('/api/trips/add')
    assert response.status_code == 401


def test_trips_can_add_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post(
        '/api/trips/add',
        json={
            'name': 'Test trip',
            'from_date': '2019-09-10',
            'till_date': '2019-09-12',
            'groups': [3, 6],
        },
    )
    assert response.json
    assert response.json['trip']['name'] == 'Test trip'
    assert response.json['trip']['from_date'] == '2019-09-10'
    assert response.json['trip']['till_date'] == '2019-09-12'
    assert response.json['trip']['groups'] == [3, 6]


@pytest.mark.parametrize('name', ['', 'a' * 51])
def test_trips_add_rejects_incorrect_name(org_logged_client: FlaskClient, name: str):
    response = org_logged_client.post(
        '/api/trips/add',
        json={
            'name': name,
            'from_date': '2019-09-10',
            'till_date': '2019-09-12',
            'groups': [3, 6],
        },
    )
    assert response.status_code == 400

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


@pytest.mark.parametrize(
    'dates',
    [('2019-09-42', '2019-09-56'), ('2019-09-10', '2019-09-08')],
)
def test_trips_add_rejects_incorrect_dates(
    org_logged_client: FlaskClient, dates: list[str]
):
    response = org_logged_client.post(
        '/api/trips/add',
        json={
            'name': 'Test trip',
            'from_date': dates[0],
            'till_date': dates[1],
            'groups': [3, 6],
        },
    )
    assert response.status_code == 400

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


@pytest.mark.parametrize(
    'groups',
    [
        [],
        [3, 0],
        [3, -6],
        ['nan', 4],
    ],
)
def test_trips_add_rejects_incorrect_groups(
    org_logged_client: FlaskClient, groups: list[Any]
):
    data = {
        'name': 'Test trip',
        'from_date': '2019-09-10',
        'till_date': '2019-09-12',
        'groups': groups
    }
    response = org_logged_client.post('/api/trips/add', json=data)
    assert response.status_code == 400

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip
