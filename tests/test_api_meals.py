from flask import Flask

from organizer.api import Units
from organizer.db import get_session
from organizer.schema import MealRecord, Trip


def test_api_rejects_adding_without_logged_in(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 0,
                             'day_number': 1,
                             'mass': 10,
                             'unit': Units.GRAMMS.value,
                             'product_id': 1
                         })
    assert result.status_code == 403


def test_api_rejects_adding_insufficient_privilegies(user_logged_client):
    result = user_logged_client.post('/api/v1/meals/add',
                                     data={
                                         'trip_id': 1,
                                         'meal_name': 0,
                                         'day_number': 1,
                                         'mass': 10,
                                         'unit': Units.GRAMMS.value,
                                         'product_id': 1
                                     })
    assert result.status_code == 403


def test_api_rejects_removing_without_logged_in(client):
    result = client.delete('/api/v1/meals/remove',
                           data={
                               'meal_id': 1
                           })
    assert result.status_code == 403


def test_api_rejects_removing_insufficient_privilegies(user_logged_client):
    result = user_logged_client.delete('/api/v1/meals/remove',
                                       data={
                                           'meal_id': 1
                                       })
    assert result.status_code == 403


def test_api_add_uses_correct_method(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 0,
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert result.status_code == 200


def test_api_add_adds_a_product_successfully(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                      MealRecord.meal_number == 0,
                                                      MealRecord.day_number == 1,
                                                      MealRecord.mass == 987,
                                                      MealRecord.product_id == 5).first()
            assert not record

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 987,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 5
                                    })

    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                      MealRecord.meal_number == 0,
                                                      MealRecord.day_number == 1,
                                                      MealRecord.mass == 987,
                                                      MealRecord.product_id == 5).first()
            assert record

    result = org_logged_client.get('/meals/1')
    assert b'987' in result.data
    assert b'Borsch concentrate' in result.data


def test_api_add_merges_existing_product(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                      MealRecord.meal_number == 0,
                                                      MealRecord.day_number == 1,
                                                      MealRecord.mass == 60,
                                                      MealRecord.product_id == 1).first()
            assert record

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 442,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            # 442 + existing 60 for multigrain cereal
            record = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                      MealRecord.meal_number == 0,
                                                      MealRecord.day_number == 1,
                                                      MealRecord.mass == 442 + 60,
                                                      MealRecord.product_id == 1).first()
            assert record


def test_api_add_adds_a_product_with_pcs(org_logged_client, app: Flask):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 5,
                                        'unit': Units.PIECES.value,
                                        'product_id': 9
                                    })
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                      MealRecord.meal_number == 0,
                                                      MealRecord.day_number == 1,
                                                      MealRecord.mass == 5 * 5.5,
                                                      MealRecord.product_id == 9).first()
            assert record

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 9
                                    })
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                      MealRecord.meal_number == 0,
                                                      MealRecord.day_number == 1,
                                                      MealRecord.mass == 5 * 5.5 + 10,
                                                      MealRecord.product_id == 9).first()
            assert record


def test_api_add_returns_fail_on_incorrect_trip_id(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 'not a number',
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 982,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_meal_name(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 256,
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'nan',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_day_number(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 287,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 'nan',
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_mass(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': -250,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 'nan',
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_unit(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': 'squirrels',
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': 999,
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.PIECES.value,
                                        'product_id': 1
                                    })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_product_id(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 487
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 'numbers'
                                    })
    assert not result.json['result']


def test_api_add_returns_fail_on_archived_product_id(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 15
                                    })
    assert not result.json['result']


def test_api_add_updates_trip(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            first_time = trip.last_update

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 987,
                                        'unit': Units.GRAMMS.value,
                                        'product_id': 5
                                    })

    assert result.status_code == 200

    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            assert first_time != trip.last_update


def test_api_remove_uses_correct_method(org_logged_client):
    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={
                                          'meal_id': 1
                                      })
    assert result.status_code == 200


def test_api_remove_removes(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.id == 1).first()
            assert record

    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={
                                          'meal_id': 1
                                      })
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            record = session.query(MealRecord).filter(MealRecord.id == 1).first()
            assert not record


def test_api_remove_rejects_incorrect_data(org_logged_client):
    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={})
    assert result.status_code == 400

    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={'meal_id': -900})
    assert result.status_code == 200
    assert not result.json['result']

    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={'meal_id': 900})
    assert result.status_code == 200
    assert not result.json['result']

    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={'meal_id': 'nan'})
    assert result.status_code == 400


def test_api_remove_updates_trip(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            first_time = trip.last_update

    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={'meal_id': 1})
    assert result.status_code == 200

    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            assert first_time != trip.last_update


def test_api_calculate_averages_reject_insufficient_privilegies(client):
    result = client.get('/api/v1/meals/averages',
                                    data={'trip_id': 1})
    assert result.status_code == 403


def test_api_requires_trip_id(user_logged_client):
    result = user_logged_client.get('/api/v1/meals/averages')
    assert result.status_code == 400


def test_api_rejects_incorrect_trip_id(user_logged_client):
    result = user_logged_client.get('/api/v1/meals/averages',
                                    query_string={'trip_id': 127})
    assert result.status_code == 404


def test_api_calculates_averages(user_logged_client):
    result = user_logged_client.get('/api/v1/meals/averages',
                                    query_string={'trip_id': 1})
    assert result.status_code == 200
    assert result.json['mass']
    assert result.json['cals']


def test_api_clear_rejects_insufficient_privilegies(user_logged_client):
    result = user_logged_client.delete('/api/v1/meals/clear',
                                       data={'trip_id': 1, 'day_number': 1})
    assert result.status_code == 403


def test_api_clear_clears(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            records = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                       MealRecord.day_number == 1).all()
            assert len(records) > 0

    result = org_logged_client.delete('/api/v1/meals/clear',
                                      data={'trip_id': 1, 'day_number': 1})
    assert result.status_code == 200
    assert result.json['result']

    with app.app_context():
        with get_session() as session:
            records = session.query(MealRecord).filter(MealRecord.trip_id == 1,
                                                       MealRecord.day_number == 1).all()
            assert len(records) == 0


def test_api_clear_rejects_incorrect_data(org_logged_client):
    result = org_logged_client.delete('/api/v1/meals/clear',
                                       data={'day_number': 1})
    assert result.status_code == 400

    result = org_logged_client.delete('/api/v1/meals/clear',
                                       data={'trip_id': 'yes'})
    assert result.status_code == 400

    result = org_logged_client.delete('/api/v1/meals/clear',
                                       data={'trip_id': 'yes',
                                             'day_number': 1})
    assert result.status_code == 400

    result = org_logged_client.delete('/api/v1/meals/clear',
                                      data={'trip_id': 1,
                                            'day_number': 'yes'})
    assert result.status_code == 400


def test_api_clear_updates_trip(org_logged_client, app: Flask):
    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            first_time = trip.last_update

    result = org_logged_client.delete('/api/v1/meals/clear',
                                      data={'trip_id': 1,
                                            'day_number': 1})
    assert result.status_code == 200

    with app.app_context():
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == 1).one()
            assert first_time != trip.last_update
