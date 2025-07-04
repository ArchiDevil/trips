from datetime import date, datetime, timedelta, timezone

from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import SharingLink, Trip, TripAccess, MealRecord
from organizer.strings import STRING_TABLE


def test_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/api/trips/')
    assert response.status_code == 401


def test_can_get_trips_for_manager(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/')
    assert response.status_code == 200
    assert response.json
    assert len(response.json) == 1
    assert response.json[0]['uid'] == 'uid1'
    assert response.json[0]['type'] == 'user'
    assert response.json[0]['attendees'] == 5
    assert response.json[0]['open_link'] == '/meals/uid1'
    assert response.json[0]['forget_link'] == '/trips/forget/uid1'

    assert response.json[0]['trip']['name'] == 'Taganay trip'
    assert response.json[0]['trip']['from_date'] == '2019-01-01'
    assert response.json[0]['trip']['till_date'] == '2019-01-05'
    assert response.json[0]['trip']['days_count'] == 5
    assert response.json[0]['trip']['created_by'] == 2
    assert response.json[0]['trip']['archived'] is False
    assert response.json[0]['trip']['groups'] == [2, 3]
    assert response.json[0]['trip']['user'] == 'Organizer'
    assert response.json[0]['trip']['edit_link'] == '/api/trips/edit/uid1'
    assert response.json[0]['trip']['share_link'] == '/api/trips/share/uid1'
    assert response.json[0]['trip']['archive_link'] == '/api/trips/archive/uid1'
    assert response.json[0]['trip']['packing_link'] == '/reports/packing/uid1'
    assert response.json[0]['trip']['shopping_link'] == '/reports/shopping/uid1'
    assert response.json[0]['trip']['download_link'] == '/api/trips/download/uid1'



def test_can_get_shared_trips(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.get('/api/trips/')
    assert response.status_code == 200
    assert response.json
    assert len(response.json) == 2
    assert response.json[0]['uid'] == 'uid1'
    assert response.json[1]['uid'] == 'uid3'


def test_trips_returns_correct_data_for_admin(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/api/trips/')
    assert response.status_code == 200
    assert response.json
    assert 2 == len(response.json)


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
    assert response.json['open_link'] == '/meals/uid1'
    assert response.json['forget_link'] == '/trips/forget/uid1'

    assert response.json['trip']['name'] == 'Taganay trip'
    assert response.json['trip']['from_date'] == '2019-01-01'
    assert response.json['trip']['till_date'] == '2019-01-05'
    assert response.json['trip']['days_count'] == 5
    assert response.json['trip']['created_by'] == 2
    assert response.json['trip']['archived'] is False
    assert response.json['trip']['groups'] == [2, 3]
    assert response.json['trip']['user'] == 'Organizer'
    assert response.json['trip']['edit_link'] == '/api/trips/edit/uid1'
    assert response.json['trip']['share_link'] == '/api/trips/share/uid1'
    assert response.json['trip']['archive_link'] == '/api/trips/archive/uid1'
    assert response.json['trip']['packing_link'] == '/reports/packing/uid1'
    assert response.json['trip']['shopping_link'] == '/reports/shopping/uid1'
    assert response.json['trip']['download_link'] == '/api/trips/download/uid1'


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
            link2 = session.query(SharingLink).one()
            assert link2.uuid == uuid
            assert (
                link2.expiration_date.day == (datetime.now(timezone.utc) + timedelta(days=3)).day
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
            link = (
                session.query(SharingLink)
                .where(SharingLink.uuid == response.json['uuid'])
                .one()
            )
            first_time = link.expiration_date

    response = org_logged_client.get('/api/trips/share/uid1')
    assert response.status_code == 200
    assert response.json

    with org_logged_client.application.app_context():
        with get_session() as session:
            link = (
                session.query(SharingLink)
                .where(SharingLink.uuid == response.json['uuid'])
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
            trip = session.query(Trip).where(Trip.uid == 'uid1').one()
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


@pytest.mark.parametrize('json_data', [
    {},
    {
        'name': '',
        'from_date': '2019-09-10',
        'till_date': '2019-09-12',
        'groups': [3, 6],
    },
    {
        'name': 'a' * 51,
        'from_date': '2019-09-10',
        'till_date': '2019-09-12',
        'groups': [3, 6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-42',
        'till_date': '2019-09-56',
        'groups': [3, 6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-10',
        'till_date': '2019-09-08',
        'groups': [3, 6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-10',
        'till_date': '2019-09-12',
        'groups': [],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-10',
        'till_date': '2019-09-12',
        'groups': [3, 0],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-10',
        'till_date': '2019-09-12',
        'groups': [3, -6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-10',
        'till_date': '2019-09-12',
        'groups': ['nan', 4],
    }
])
def test_trips_add_rejects_incorrect_data(org_logged_client: FlaskClient, json_data: dict):
    response = org_logged_client.post('/api/trips/add', json=json_data)
    assert response.status_code == 400

    if json_data.get('name'):
        with org_logged_client.application.app_context():
            with get_session() as session:
                trip = session.query(Trip).where(Trip.name == json_data.get('name')).first()
                assert not trip


def test_trips_edit_rejects_not_logged_in(client: FlaskClient):
    response = client.post('/api/trips/edit/1')
    assert response.status_code == 401


def test_trips_edit_rejects_insufficient_privileges(org_logged_client: FlaskClient):
    response = org_logged_client.post(
        '/api/trips/edit/uid3',
        json={
            'name': 'Test trip',
            'from_date': '2019-10-09',
            'till_date': '2019-10-12',
            'groups': [3, 6],
        },
    )
    assert response.status_code == 403

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip = session.query(Trip).where(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_edit_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post(
        '/api/trips/edit/uid100',
        json={
            'name': 'Test trip',
            'from_date': '2019-10-09',
            'till_date': '2019-10-12',
            'groups': [3, 6],
        },
    )
    assert response.status_code == 404


def test_trips_can_edit_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post(
        '/api/trips/edit/uid1',
        json={
            'name': 'Test trip',
            'from_date': '2019-10-09',
            'till_date': '2019-10-12',
            'groups': [3, 6],
        },
    )
    assert response.status_code == 200
    assert response.json
    assert response.json['uid'] == 'uid1'

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip = session.query(Trip).where(Trip.name == 'Test trip').one()
            assert trip.from_date == date(2019, 10, 9)
            assert trip.till_date == date(2019, 10, 12)
            assert trip.groups[0].persons == 3
            assert trip.groups[1].persons == 6


def test_trips_can_edit_shared_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.post(
        '/api/trips/edit/uid1',
        json={
            'name': 'Test trip',
            'from_date': '2019-10-09',
            'till_date': '2019-10-12',
            'groups': [3, 6],
        },
    )
    assert response.status_code == 200
    assert response.json
    assert response.json['uid'] == 'uid1'

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip = session.query(Trip).where(Trip.name == 'Test trip').one()
            assert trip.from_date == date(2019, 10, 9)
            assert trip.till_date == date(2019, 10, 12)
            assert trip.groups[0].persons == 3
            assert trip.groups[1].persons == 6


def test_trips_admin_can_edit_any_trip(admin_logged_client: FlaskClient):
    response = admin_logged_client.post(
        '/api/trips/edit/uid1',
        json={
            'name': 'Test trip',
            'from_date': '2019-10-09',
            'till_date': '2019-10-12',
            'groups': [3, 6],
        },
    )
    assert response.status_code == 200
    assert response.json
    assert response.json['uid'] == 'uid1'

    with admin_logged_client.application.app_context():
        with get_session() as session:
            trip = session.query(Trip).where(Trip.name == 'Test trip').one()
            assert trip.from_date == date(2019, 10, 9)
            assert trip.till_date == date(2019, 10, 12)
            assert trip.groups[0].persons == 3
            assert trip.groups[1].persons == 6


@pytest.mark.parametrize('json_data', [
    {},
    {
        'name': '',
        'from_date': '2019-10-09',
        'till_date': '2019-10-12',
        'groups': [3, 6],
    },
    {
        'name': 'a' * 51,
        'from_date': '2019-10-09',
        'till_date': '2019-10-12',
        'groups': [3, 6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-42',
        'till_date': '2019-09-56',
        'groups': [3, 6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-09-10',
        'till_date': '2019-09-08',
        'groups': [3, 6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-10-09',
        'till_date': '2019-10-12',
        'groups': [],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-10-09',
        'till_date': '2019-10-12',
        'groups': [3, 0],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-10-09',
        'till_date': '2019-10-12',
        'groups': [3, -6],
    },
    {
        'name': 'Test trip',
        'from_date': '2019-10-09',
        'till_date': '2019-10-12',
        'groups': ['nan', 4],
    },
])
def test_trips_edit_rejects_incorrect_data(org_logged_client: FlaskClient, json_data: dict):
    response = org_logged_client.post('/api/trips/edit/uid1', json=json_data)
    assert response.status_code == 400

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip = session.query(Trip).where(Trip.name == 'Taganay trip').one()
            assert trip.from_date == date(2019, 1, 1)
            assert trip.till_date == date(2019, 1, 5)
            assert trip.groups[0].persons == 2
            assert trip.groups[1].persons == 3


def test_trips_download_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/api/trips/download/uid1')
    assert response.status_code == 401


def test_trips_download_allows_non_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/download/uid3')
    assert response.status_code == 200


def test_trips_download_returns_csv(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/download/uid1')
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


def test_trips_can_download_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/download/uid3')
    assert response.status_code == 200
    assert response.data

    data: str = response.data[3:].decode(encoding='utf-8')
    lines = data.splitlines()
    assert lines
    assert len(lines) == 2
    assert lines[0] == ','.join([
        STRING_TABLE['CSV name'],
        STRING_TABLE['CSV day'],
        STRING_TABLE['CSV meal'],
        STRING_TABLE['CSV mass'],
        STRING_TABLE['CSV cals']
    ])
    assert ','.join([
        'Multigrain cereal', '1', STRING_TABLE['Meals breakfast title'], '60', '362.0'
    ]) in lines


def test_trips_download_returns_empty_csv(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/api/trips/download/uid3')
    assert response.status_code == 200
    assert response.data

    # skip BOM
    data: str = response.data[3:].decode(encoding='utf-8')
    lines = data.splitlines()
    assert lines
    assert len(lines) == 2
    assert lines[0] == ','.join([
        STRING_TABLE['CSV name'],
        STRING_TABLE['CSV day'],
        STRING_TABLE['CSV meal'],
        STRING_TABLE['CSV mass'],
        STRING_TABLE['CSV cals']
    ])


def test_trips_download_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/trips/download/uid42')
    assert response.status_code == 404


def test_trips_copy_rejects_not_logged_in(client: FlaskClient):
    response = client.post('/api/trips/copy/uid1')
    assert response.status_code == 401


def test_trips_copy_rejects_empty_json(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/copy/uid1', json={})
    assert response.status_code == 400


def test_trips_copy_rejects_empty_name(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/copy/uid1', json={'name': ''})
    assert response.status_code == 400


def test_trips_copy_rejects_missing_name(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/copy/uid1', json={'nonexisting': 'field'})
    assert response.status_code == 400


def test_trips_copy_rejects_non_existing_trip_id(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/copy/uid100', json={'name': 'New trip'})
    assert response.status_code == 404


def test_trips_copy_rejects_not_owned_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/copy/uid3', json={'name': 'New trip'})
    assert response.status_code == 403


def test_trips_can_copy(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/trips/copy/uid1', json={'name': 'New trip'})
    assert response.status_code == 200
    assert response.json and response.json['uid'] is not None

    with org_logged_client.application.app_context():
        with get_session() as session:
            old_records = session.query(MealRecord).where(MealRecord.trip_id == 1).all()
            new_records = session.query(MealRecord).where(MealRecord.trip_id == 4).all()
            assert len(old_records) == len(new_records)
