from datetime import date
from typing import Dict
from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import Trip, TripAccess
from organizer.strings import STRING_TABLE


def test_trips_edit_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/edit/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_edit_rejects_insufficient_privileges(org_logged_client: FlaskClient):
    response = org_logged_client.post('/trips/edit/uid3',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert response.status_code == 403

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_can_see_edit_trip_page(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/edit/uid1')
    assert response.status_code == 200
    assert STRING_TABLE['Trips edit edit button'].encode() in response.data
    assert STRING_TABLE['Trips edit archive button'].encode() in response.data


def test_trips_edit_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/edit/uid100')
    assert response.status_code == 404


def test_trips_can_edit_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/trips/edit/uid1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert response.status_code == 302

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').one()
            assert trip.from_date == date(2019, 9, 10)
            assert trip.till_date == date(2019, 9, 12)
            assert trip.groups[0].persons == 3
            assert trip.groups[1].persons == 6


def test_trips_can_edit_shared_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.post('/trips/edit/uid1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert response.status_code == 302

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').one()
            assert trip.from_date == date(2019, 9, 10)
            assert trip.till_date == date(2019, 9, 12)
            assert trip.groups[0].persons == 3
            assert trip.groups[1].persons == 6


def test_trips_admin_can_edit_any_trip(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/trips/edit/uid1',
                                        data={
                                            'name': 'Test trip',
                                            'daterange': '10-09-2019 - 12-09-2019',
                                            'group1': '3',
                                            'group2': '6',
                                            'redirect': '/'
                                        })
    assert response.status_code == 302

    with admin_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(
                Trip.name == 'Test trip').one()
            assert trip.from_date == date(2019, 9, 10)
            assert trip.till_date == date(2019, 9, 12)
            assert trip.groups[0].persons == 3
            assert trip.groups[1].persons == 6


def test_trips_redirects_correctly(org_logged_client: FlaskClient):
    response = org_logged_client.post('/trips/edit/uid1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/test.html'
                                      })
    assert response.status_code == 302
    assert '/test.html' in response.location


def test_trips_redirect_created_if_provided(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/edit/uid1', headers={'Referer': 'test.com'})
    assert response.status_code == 200
    assert 'name="redirect" value="test.com"' in response.data.decode(encoding='utf-8')


def test_trips_redirect_created_if_not_provided(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/edit/uid1')
    assert response.status_code == 200
    assert 'name="redirect" value="/trips/"' in response.data.decode(encoding='utf-8')


@pytest.mark.parametrize('name', ['', 'a' * 51])
def test_trips_edit_rejects_wrong_name(org_logged_client: FlaskClient, name: str):
    response = org_logged_client.post('/trips/edit/uid1',
                                      data={
                                          'name': name,
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect name'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Taganay trip').one()
            assert trip.from_date == date(2019, 1, 1)
            assert trip.till_date == date(2019, 1, 5)
            assert trip.groups[0].persons != 3
            assert trip.groups[1].persons != 6


@pytest.mark.parametrize('dates', ['2019-09-10 ! 2019-09-12',
                                   '42-09-2019 - 56-09-2019',
                                   '10-09-2019 - 08-09-2019'])
def test_trips_edit_rejects_incorrect_dates(org_logged_client: FlaskClient, dates: str):
    response = org_logged_client.post('/trips/edit/uid1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': dates,
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Taganay trip').one()
            assert trip.from_date == date(2019, 1, 1)
            assert trip.till_date == date(2019, 1, 5)
            assert trip.groups[0].persons != 3
            assert trip.groups[1].persons != 6


def test_trips_edit_shows_redirect_error(org_logged_client: FlaskClient):
    response = org_logged_client.post('/trips/edit/uid1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '08-09-2019 - 10-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert response.status_code == 200
    assert b'No redirect field is provided' in response.data


@pytest.mark.parametrize('groups', [{},
                                    {'group1': '3', 'group2': '0'},
                                    {'group1': '3', 'group2': '-6'},
                                    {'group1': 'nan', 'group2': '4'}])
def test_trips_edit_rejects_empty_groups(org_logged_client: FlaskClient, groups: Dict[str, str]):
    data = {'name': 'Test trip',
            'daterange': '10-09-2019 - 12-09-2019',
            'redirect': '/'}
    data.update(groups)

    response = org_logged_client.post('/trips/edit/uid1',
                                      data=data)
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Taganay trip').one()
            assert trip.from_date == date(2019, 1, 1)
            assert trip.till_date == date(2019, 1, 5)
            assert trip.groups[0].persons == 2
            assert trip.groups[1].persons == 3
