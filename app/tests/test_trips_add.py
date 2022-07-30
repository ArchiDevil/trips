from datetime import date
from flask.testing import FlaskClient
import pytest
from typing import Dict

from organizer.db import get_session
from organizer.schema import Trip
from organizer.strings import STRING_TABLE


def test_trips_add_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/add')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_can_see_add_trip_page(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/add')
    assert response.status_code == 200
    assert STRING_TABLE['Trips add edit button'].encode() in response.data


def test_trips_can_add_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert response.status_code == 302

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').one()
            assert trip.from_date == date(2019, 9, 10)
            assert trip.till_date == date(2019, 9, 12)
            assert trip.groups[0].persons == 3
            assert trip.groups[1].persons == 6


@pytest.mark.parametrize('name', ['', 'a' * 51])
def test_trips_add_rejects_incorrect_name(org_logged_client: FlaskClient, name: str):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': name,
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect name'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


@pytest.mark.parametrize('dates', ['2019-09-10 ! 2019-09-12',
                                   '42-09-2019 - 56-09-2019',
                                   '10-09-2019 - 08-09-2019'])
def test_trips_add_rejects_incorrect_dates(org_logged_client: FlaskClient, dates: str):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': dates,
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


@pytest.mark.parametrize('groups', [{},
                                    {'group1': '3', 'group2': '0'},
                                    {'group1': '3', 'group2': '-6'},
                                    {'group1': 'nan', 'group2': '4'}])
def test_trips_add_rejects_incorrect_groups(org_logged_client: FlaskClient, groups: Dict[str, str]):
    data = {
        'name': 'Test trip',
        'daterange': '10-09-2019 - 12-09-2019'
    }
    data.update(groups)
    response = org_logged_client.post('/trips/add',
                                      data=data)
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip
