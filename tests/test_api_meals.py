# TODO: check that trip was touched somehow
# TODO: check if product was really added somehow
# TODO: check if record was removed somehow


def test_api_add_uses_correct_method(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 0,
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert result.status_code == 200


def test_api_add_adds_a_product_successfully(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    # TODO: actually, it is not possible to inderstand if product was added or not
    assert result.json['result']


def test_api_add_adds_a_product_with_pcs(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 5,
                             'unit': 'pcs',
                             'product_id': 9
                         })
    # TODO: actually, it is not possible to inderstand if product was added or not
    assert result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 9
                         })
    # TODO: actually, it is not possible to inderstand if product was added or not
    assert result.json['result']


def test_api_add_returns_fail_on_incorrect_trip_id(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 'not a number',
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 982,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_meal_name(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 256,
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'nan',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_day_number(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 287,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 'nan',
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_mass(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': -250,
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 'nan',
                             'unit': 'grams',
                             'product_id': 1
                         })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_unit(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'squirrels',
                             'product_id': 1
                         })
    assert not result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 999,
                             'product_id': 1
                         })
    assert not result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'pcs',
                             'product_id': 1
                         })
    assert not result.json['result']


def test_api_add_returns_fail_on_incorrect_product_id(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 487
                         })
    assert not result.json['result']

    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 'numbers'
                         })
    assert not result.json['result']


def test_api_add_returns_fail_on_archived_product_id(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 'breakfast',
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
                             'product_id': 15
                         })
    assert not result.json['result']


def test_api_remove_uses_correct_method(client):
    result = client.delete('/api/v1/meals/remove',
                           data={
                               'meal_id': 1
                           })
    assert result.status_code == 200


def test_api_remove_removes_meal_record(client):
    result = client.delete('/api/v1/meals/remove',
                           data={
                               'meal_id': 1
                           })
    assert result.json['result']


def test_api_remove_returns_fail_on_incorrect_meal_id(client):
    result = client.delete('/api/v1/meals/remove',
                           data={'meal_id': -900})
    assert not result.json['result']

    result = client.delete('/api/v1/meals/remove',
                           data={'meal_id': 900})
    assert not result.json['result']

    result = client.delete('/api/v1/meals/remove',
                           data={'meal_id': 'nan'})
    assert not result.json['result']