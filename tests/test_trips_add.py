from datetime import date
from werkzeug.test import Client

from organizer.db import get_session
from organizer.schema import Trip
from organizer.strings import STRING_TABLE



def test_trips_add_rejects_not_logged_in(client: Client):
    response = client.get('/trips/add')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_add_rejects_for_guest(user_logged_client: Client):
    response = user_logged_client.get('/trips/add')
    assert response.status_code == 403


def test_trips_can_see_add_trip_page(org_logged_client: Client):
    response = org_logged_client.get('/trips/add')
    assert response.status_code == 200
    assert STRING_TABLE['Trips add edit button'].encode() in response.data


def test_trips_can_add_trip(org_logged_client: Client):
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


def test_trips_add_rejects_wrong_name(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': '',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect name'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_add_rejects_wrong_dates_format(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 ! 2019-09-12',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_add_rejects_wrong_dates_values(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '42-09-2019 - 56-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_add_rejects_swapped_dates(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 08-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_add_rejects_empty_groups(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_add_rejects_zeroes_group_values(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '0'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_add_rejects_negative_group_values(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '-6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip


def test_trips_add_rejects_nan_group_values(org_logged_client: Client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': 'nan',
                                          'group2': '4'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    with org_logged_client.application.app_context():
        with get_session() as session:
            trip: Trip = session.query(Trip).filter(Trip.name == 'Test trip').first()
            assert not trip
