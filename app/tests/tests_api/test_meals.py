import pytest

from flask import Flask
from flask.testing import FlaskClient

from organizer.db import get_session
from organizer.schema import MealRecord, Trip, TripAccess, Units


def test_api_rejects_adding_without_logged_in(client: FlaskClient):
    result = client.post(
        '/api/meals/add',
        data={
            'trip_id': 1,
            'meal_name': 0,
            'day_number': 1,
            'mass': 10,
            'unit': Units.GRAMMS.value,
            'product_id': 1,
        },
    )
    assert result.status_code == 401


def test_api_rejects_adding_for_non_owned_trip(org_logged_client: FlaskClient):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid3',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 5,
            'unit': Units.GRAMMS.value,
            'product_id': 9,
        },
    )
    assert result.status_code == 403


def test_api_rejects_removing_without_logged_in(client: FlaskClient):
    result = client.delete('/api/meals/remove', data={'meal_id': 1})
    assert result.status_code == 401


def test_api_rejects_removing_for_non_owned_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(
                MealRecord(
                    trip_id=3, product_id=5, day_number=1, meal_number=1, mass=50
                )
            )
            session.commit()

            rec = session.query(MealRecord).filter(MealRecord.trip_id == 3).first()
            assert rec
            meal_id = rec.id

    result = org_logged_client.delete('/api/meals/remove', json={'meal_id': meal_id})
    assert result.status_code == 403


def test_api_add_adds_product(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 1,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 987,
                    MealRecord.product_id == 5,
                )
                .first()
            )
            assert not record

    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 987,
            'unit': Units.GRAMMS.value,
            'product_id': 5,
        },
    )

    assert result.json
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 1,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 987,
                    MealRecord.product_id == 5,
                )
                .first()
            )
            assert record


def test_api_add_adds_product_to_shared_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 1,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 987,
                    MealRecord.product_id == 5,
                )
                .first()
            )
            assert not record

    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid3',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 987,
            'unit': Units.GRAMMS.value,
            'product_id': 5,
        },
    )

    assert result.json
    assert result.json['result']

    with org_logged_client.application.app_context():
        with get_session() as session:
            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 3,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 987,
                    MealRecord.product_id == 5,
                )
                .first()
            )
            assert record


def test_api_add_merges_existing_product(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 1,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 60,
                    MealRecord.product_id == 1,
                )
                .first()
            )
            assert record

    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 442,
            'unit': Units.GRAMMS.value,
            'product_id': 1,
        },
    )
    assert result.json
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            # 442 + existing 60 for multigrain cereal
            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 1,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 442 + 60,
                    MealRecord.product_id == 1,
                )
                .first()
            )
            assert record


def test_api_add_adds_a_product_with_pcs(org_logged_client: FlaskClient, app: Flask):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 5,
            'unit': Units.PIECES.value,
            'product_id': 9,
        },
    )
    assert result.json
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 1,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 5 * 5.5,
                    MealRecord.product_id == 9,
                )
                .first()
            )
            assert record


def test_api_add_merges_product_with_pcs(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            session.add(
                MealRecord(
                    trip_id=1, meal_number=0, day_number=1, mass=5 * 5.5, product_id=9
                )
            )
            session.commit()

    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 10,
            'unit': Units.GRAMMS.value,
            'product_id': 9,
        },
    )
    assert result.json
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = (
                session.query(MealRecord)
                .filter(
                    MealRecord.trip_id == 1,
                    MealRecord.meal_number == 0,
                    MealRecord.day_number == 1,
                    MealRecord.mass == 5 * 5.5 + 10,
                    MealRecord.product_id == 9,
                )
                .first()
            )
            assert record


def test_api_add_rejects_incorrect_request(org_logged_client: FlaskClient):
    result = org_logged_client.post('/api/meals/add')
    assert result.status_code == 415


@pytest.mark.parametrize('trip_id', ['not a number', 982])
def test_api_add_returns_fail_on_incorrect_trip_id(
    org_logged_client: FlaskClient, trip_id
):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': trip_id,
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 10,
            'unit': Units.GRAMMS.value,
            'product_id': 1,
        },
    )
    assert result.json
    assert not result.json['result']


@pytest.mark.parametrize('name', [256, 'nan'])
def test_api_add_returns_fail_on_incorrect_meal_name(
    org_logged_client: FlaskClient, name
):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': name,
            'day_number': 1,
            'mass': 10,
            'unit': Units.GRAMMS.value,
            'product_id': 1,
        },
    )
    assert result.json
    assert not result.json['result']


@pytest.mark.parametrize('day', [256, 'nan'])
def test_api_add_returns_fail_on_incorrect_day_number(
    org_logged_client: FlaskClient, day
):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': day,
            'mass': 10,
            'unit': Units.GRAMMS.value,
            'product_id': 1,
        },
    )
    assert result.json
    assert not result.json['result']


@pytest.mark.parametrize('mass', [-250, 'nan'])
def test_api_add_returns_fail_on_incorrect_mass(org_logged_client: FlaskClient, mass):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': mass,
            'unit': Units.GRAMMS.value,
            'product_id': 1,
        },
    )
    assert result.json
    assert not result.json['result']


@pytest.mark.parametrize('unit', [999, 'squirrels', Units.PIECES.value])
def test_api_add_returns_fail_on_incorrect_unit(org_logged_client: FlaskClient, unit):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 10,
            'unit': unit,
            'product_id': 1,
        },
    )
    assert result.json
    assert not result.json['result']


@pytest.mark.parametrize('product', [999, 'numbers'])
def test_api_add_returns_fail_on_incorrect_product_id(
    org_logged_client: FlaskClient, product
):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 10,
            'unit': Units.GRAMMS.value,
            'product_id': product,
        },
    )
    assert result.json
    assert not result.json['result']


def test_api_add_returns_fail_on_archived_product_id(org_logged_client: FlaskClient):
    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 10,
            'unit': Units.GRAMMS.value,
            'product_id': 15,
        },
    )
    assert result.json
    assert not result.json['result']


def test_api_add_updates_trip(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            first_time = trip.last_update

    result = org_logged_client.post(
        '/api/meals/add',
        json={
            'trip_uid': 'uid1',
            'meal_name': 'breakfast',
            'day_number': 1,
            'mass': 987,
            'unit': Units.GRAMMS.value,
            'product_id': 5,
        },
    )

    assert result.status_code == 200

    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            assert first_time != trip.last_update


def test_api_remove_removes(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.id == 1).first()
            assert record

    result = org_logged_client.delete('/api/meals/remove', json={'meal_id': 1})
    assert result.status_code == 200
    assert result.json
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.id == 1).first()
            assert not record


def test_api_remove_removes_shared_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()
            rec_id = (
                session.query(MealRecord)
                .filter(MealRecord.trip_id == 3, MealRecord.day_number == 1)
                .one()
                .id
            )

    result = org_logged_client.delete('/api/meals/remove', json={'meal_id': rec_id})
    assert result.status_code == 200
    assert result.json
    assert result.json['result']

    with org_logged_client.application.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.id == rec_id).first()
            assert not record


@pytest.mark.parametrize('meal_id', ['nan', None])
def test_api_remove_rejects_incorrect_data(org_logged_client: FlaskClient, meal_id):
    result = org_logged_client.delete(
        '/api/meals/remove', json={'meal_id': meal_id} if meal_id is not None else {}
    )
    assert result.status_code == 400


@pytest.mark.parametrize('meal_id', [-900, 900])
def test_api_remove_returns_fail_on_incorrect_meal_id(
    org_logged_client: FlaskClient, meal_id
):
    result = org_logged_client.delete('/api/meals/remove', json={'meal_id': meal_id})
    assert result.status_code == 200
    assert result.json
    assert not result.json['result']


def test_api_remove_updates_trip(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            first_time = trip.last_update

    result = org_logged_client.delete('/api/meals/remove', json={'meal_id': 1})
    assert result.status_code == 200

    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            assert first_time != trip.last_update


def test_api_clear_rejects_incorrect_request(org_logged_client: FlaskClient):
    result = org_logged_client.post('/api/meals/clear')
    assert result.status_code == 415


def test_api_clear_rejects_for_non_owned_trip(org_logged_client: FlaskClient):
    result = org_logged_client.post(
        '/api/meals/clear', json={'trip_uid': 'uid3', 'day_number': 1}
    )
    assert result.status_code == 403


def test_api_clear_rejects_non_existing_trip(org_logged_client: FlaskClient):
    result = org_logged_client.post(
        '/api/meals/clear', json={'trip_uid': 'uid999', 'day_number': 1}
    )
    assert result.status_code == 404


def test_api_clear_clears(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            records = (
                session.query(MealRecord)
                .filter(MealRecord.trip_id == 1, MealRecord.day_number == 1)
                .all()
            )
            assert len(records) > 0

    result = org_logged_client.post(
        '/api/meals/clear', json={'trip_uid': 'uid1', 'day_number': 1}
    )
    assert result.status_code == 200
    assert result.json
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            records = (
                session.query(MealRecord)
                .filter(MealRecord.trip_id == 1, MealRecord.day_number == 1)
                .all()
            )
            assert len(records) == 0


def test_api_clear_shared_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    result = org_logged_client.post(
        '/api/meals/clear', json={'trip_uid': 'uid3', 'day_number': 1}
    )
    assert result.status_code == 200
    assert result.json
    assert result.json['result']

    with org_logged_client.application.app_context():
        with get_session() as session:
            records = (
                session.query(MealRecord)
                .filter(MealRecord.trip_id == 3, MealRecord.day_number == 1)
                .all()
            )
            assert len(records) == 0


@pytest.mark.parametrize(
    'json',
    [{'day_number': 1}, {'trip_uid': 'yes'}, {'trip_uid': 'uid1', 'day_number': 'yes'}],
)
def test_api_clear_rejects_incorrect_data(org_logged_client: FlaskClient, json):
    result = org_logged_client.post('/api/meals/clear', json=json)
    assert result.status_code == 400


def test_api_clear_updates_trip(org_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            first_time = trip.last_update

    result = org_logged_client.post(
        '/api/meals/clear', json={'trip_uid': 'uid1', 'day_number': 1}
    )
    assert result.status_code == 200

    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            assert first_time != trip.last_update


def test_get_trip_meals_rejects_not_logged_in(client: FlaskClient):
    result = client.get('/api/meals/1')
    assert result.status_code == 401


def test_get_trip_meals_rejects_incorrect_data(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/meals/555')
    assert result.status_code == 404


def test_get_trip_meals_returns_meals(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/meals/uid1')
    assert response.status_code == 200
    assert response.json
    assert 'days' in response.json
    assert 5 == len(response.json['days'])


def test_get_trip_meals_allows_non_owned_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/meals/uid3')
    assert response.status_code == 200


def test_get_trip_meals_works_for_admin(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/api/meals/uid1')
    assert response.status_code == 200


def test_get_trip_meals_returns_data_for_shared_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.get('/api/meals/uid3')
    assert response.status_code == 200
    assert response.json
    assert response.json['days']
    assert 3 == len(response.json['days'])


def test_get_trip_day_meals_rejects_not_logged_in(client: FlaskClient):
    result = client.get('/api/meals/1/1')
    assert result.status_code == 401


@pytest.mark.parametrize(
    'trip_id, day_number', [(1, 200), (42, 1), (200, 200), (-100200, 200)]
)
def test_get_trip_day_meals_rejects_incorrect_ids(
    org_logged_client: FlaskClient, trip_id, day_number
):
    result = org_logged_client.get(f'/api/meals/{trip_id}/{day_number}')
    assert result.status_code == 404


def test_get_trip_day_meals_allows_non_owned_trip(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/meals/uid3/1')
    assert result.status_code == 200


def test_get_trip_day_meals_returns_meals(org_logged_client: FlaskClient):
    response = org_logged_client.get('/api/meals/uid1/1')
    assert response.status_code == 200
    assert response.json
    assert 'day' in response.json
    day = response.json['day']
    assert 1 == day['number']
    assert day['meals']
    assert day['date']
    assert day['reload_link']


def test_meals_cycle_rejects_not_logged_in(client: FlaskClient):
    response = client.post('/api/meals/1/cycle',
                           json={
                               'src-start': '1',
                               'src-end': '1',
                               'dst-start': '2',
                               'dst-end': '5'
                           })
    assert response.status_code == 401


def test_meals_cycle_rejects_non_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/meals/uid3/cycle',
                                      json={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 403


def test_meals_cycle_rejects_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/meals/100/cycle',
                                      json={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 404


def test_meals_cycle_cycles(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.query(MealRecord).filter(MealRecord.day_number != 1).delete()
            session.commit()

    response = org_logged_client.post('/api/meals/uid1/cycle',
                                      json={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 200
    assert response.json == {'result': 'ok'}

    with org_logged_client.application.app_context():
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

    response = org_logged_client.post('/api/meals/uid3/cycle',
                                      json={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '3'
                                      })
    assert response.status_code == 200
    assert response.json == {'result': 'ok'}

    with org_logged_client.application.app_context():
        with get_session() as session:
            base_records = session.query(MealRecord).filter(MealRecord.trip_id == 3,
                                                            MealRecord.day_number == 1).all()
            base_size = len(base_records)

            records = session.query(MealRecord).filter(MealRecord.day_number > 1).all()
            assert len(records) == base_size * 2 # all 2 left days are filled


def test_meals_cycle_cycles_with_overwrite(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.query(MealRecord).filter(MealRecord.day_number != 1).delete()
            session.commit()

    response = org_logged_client.post('/api/meals/uid1/cycle',
                                      json={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '2'
                                      })
    assert response.status_code == 200
    assert response.json == {'result': 'ok'}

    with org_logged_client.application.app_context():
        with get_session() as session:
            # remove breakfast completely
            session.query(MealRecord).filter(MealRecord.day_number == 1,
                                             MealRecord.meal_number == 0).delete()
            session.commit()

            # we have something on breakfast on day 2
            records = session.query(MealRecord).filter(MealRecord.day_number == 2,
                                                       MealRecord.meal_number == 0).all()
            assert records

    response = org_logged_client.post('/api/meals/uid1/cycle',
                                      json={
                                          'src-start': '1',
                                          'src-end': '1',
                                          'dst-start': '2',
                                          'dst-end': '2',
                                          'overwrite': True
                                      })
    assert response.status_code == 200
    assert response.json == {'result': 'ok'}

    with org_logged_client.application.app_context():
        with get_session() as session:
            # no more data on breakfast on day 2
            records = session.query(MealRecord).filter(MealRecord.day_number == 2,
                                                       MealRecord.meal_number == 0).all()
            assert not records


def test_meals_cycle_rejects_overlapping_ranges(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/meals/uid1/cycle',
                                      json={
                                          'src-start': '1',
                                          'src-end': '3',
                                          'dst-start': '2',
                                          'dst-end': '5'
                                      })
    assert response.status_code == 400

    response = org_logged_client.post('/api/meals/uid1/cycle',
                                      json={
                                          'src-start': '3',
                                          'src-end': '5',
                                          'dst-start': '2',
                                          'dst-end': '4'
                                      })
    assert response.status_code == 400

    response = org_logged_client.post('/api/meals/uid1/cycle',
                                      json={
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
    response = org_logged_client.post('/api/meals/uid1/cycle', json=data)
    assert response.status_code == 400


@pytest.mark.parametrize('data', [
    {'src-end': '1', 'dst-start': '2', 'dst-end': '3'},
    {'src-start': '1', 'dst-start': '2', 'dst-end': '3'},
    {'src-start': '1', 'src-end': '1', 'dst-end': '3'},
    {'src-start': '1', 'src-end': '1', 'dst-start': '2'}
])
def test_meals_cycle_rejects_missing_data(org_logged_client: FlaskClient, data):
    response = org_logged_client.post('/api/meals/uid1/cycle', json=data)
    assert response.status_code == 400
