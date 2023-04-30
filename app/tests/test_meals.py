from flask import Flask
from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import MealRecord, TripAccess


def test_meals_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/meals/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_meals_shows_non_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/meals/uid3')
    assert response.status_code == 200


def test_meals_shows_page(org_logged_client: FlaskClient):
    response = org_logged_client.get('/meals/uid1')
    assert response.status_code == 200


def test_meals_show_shared_trip_page(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.get('/meals/uid3')
    assert response.status_code == 200


def test_meals_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/meals/uid100')
    assert response.status_code == 404


def test_meals_cycle_rejects_not_logged_in(client: FlaskClient):
    response = client.post('/meals/cycle_days/1',
                           data={
                               'src-start': '1',
                               'src-end': '1',
                               'dst-start': '2',
                               'dst-end': '5'
                           })
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_meals_cycle_rejects_non_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/meals/cycle_days/uid3',
                                      data={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 403


def test_meals_cycle_rejects_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/meals/cycle_days/100',
                                      data={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 404


def test_meals_cycle_cycles(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            session.query(MealRecord).filter(MealRecord.day_number != 1).delete()
            session.commit()

    response = org_logged_client.post('/meals/cycle_days/uid1',
                                      data={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 302
    assert '/meals/uid1' in response.location

    with app.app_context():
        with get_session() as session:
            base_records = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                            MealRecord.day_number == 1).all()
            base_size = len(base_records)

            records = session.query(MealRecord).filter(MealRecord.day_number > 1).all()
            assert len(records) == base_size * 4 # all 4 left days are filled


def test_meals_cycle_cycles_shared_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.query(MealRecord).filter(MealRecord.day_number != 1).delete()
            session.commit()

    response = org_logged_client.post('/meals/cycle_days/uid3',
                                      data={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '3'
                                      })
    assert response.status_code == 302
    assert '/meals/uid3' in response.location

    with org_logged_client.application.app_context():
        with get_session() as session:
            base_records = session.query(MealRecord).filter(MealRecord.trip_id == 3,
                                                            MealRecord.day_number == 1).all()
            base_size = len(base_records)

            records = session.query(MealRecord).filter(MealRecord.day_number > 1).all()
            assert len(records) == base_size * 2 # all 2 left days are filled


def test_meals_cycle_cycles_with_overwrite(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            session.query(MealRecord).filter(MealRecord.day_number != 1).delete()
            session.commit()

    response = org_logged_client.post('/meals/cycle_days/uid1',
                                      data={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '2'
                                      })
    assert response.status_code == 302

    with app.app_context():
        with get_session() as session:
            # remove breakfast completely
            session.query(MealRecord).filter(MealRecord.day_number == 1,
                                             MealRecord.meal_number == 0).delete()
            session.commit()

            # we have something on breakfast on day 2
            records = session.query(MealRecord).filter(MealRecord.day_number == 2,
                                                       MealRecord.meal_number == 0).all()
            assert records

    response = org_logged_client.post('/meals/cycle_days/uid1',
                                      data={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '2',
                                          'overwrite': '1'
                                      })
    assert response.status_code == 302

    with app.app_context():
        with get_session() as session:
            # no more data on breakfast on day 2
            records = session.query(MealRecord).filter(MealRecord.day_number == 2,
                                                       MealRecord.meal_number == 0).all()
            assert not records


def test_meals_cycle_rejects_overlapping_ranges(org_logged_client: FlaskClient):
    response = org_logged_client.post('/meals/cycle_days/uid1',
                                      data={
                                          'src-start': '1',
                                          'src-end': '3',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 400

    response = org_logged_client.post('/meals/cycle_days/uid1',
                                      data={
                                          'src-start': '3',
                                          'src-end': '5',
                                          'dst-start': '2',
                                          'dst-end': '4'
                                      })
    assert response.status_code == 400

    response = org_logged_client.post('/meals/cycle_days/uid1',
                                      data={
                                          'src-start': '2',
                                          'src-end': '4',
                                          'dst-start': '2',
                                          'dst-end': '4'
                                      })
    assert response.status_code == 400


@pytest.mark.parametrize('data', [
    {},
    {'src-start': '-10', 'src-end': '-5', 'dst-start': '-2', 'dst-end': '-15'},
    {'src-start': '1', 'src-end': '25', 'dst-start': '26', 'dst-end': '30'},
    {'src-start': '2', 'src-end': '1', 'dst-start': '2', 'dst-end': '3'},
    {'src-start': 'yes', 'src-end': '1', 'dst-start': '2', 'dst-end': '3'},
    {'src-start': '1', 'src-end': 'yes', 'dst-start': '2', 'dst-end': '3'},
    {'src-start': '1', 'src-end': '1', 'dst-start': 'yes', 'dst-end': '3'},
    {'src-start': '1', 'src-end': '1', 'dst-start': '2', 'dst-end': 'yes'}
])
def test_meals_cycle_rejects_incorrect_days(org_logged_client: FlaskClient, data):
    response = org_logged_client.post('/meals/cycle_days/uid1', data=data)
    assert response.status_code == 400


@pytest.mark.parametrize('data', [
    {'src-end': '1', 'dst-start': '2', 'dst-end': '3'},
    {'src-start': '1', 'dst-start': '2', 'dst-end': '3'},
    {'src-start': '1', 'src-end': '1', 'dst-end': '3'},
    {'src-start': '1', 'src-end': '1', 'dst-start': '2'}
])
def test_meals_cycle_rejects_missing_data(org_logged_client: FlaskClient, data):
    response = org_logged_client.post('/meals/cycle_days/uid1', data=data)
    assert response.status_code == 400
