# TODO: check that trip was touched somehow
# TODO: check if product was really added somehow
# TODO: check if record was removed somehow


def test_api_rejects_adding_without_logged_in(client):
    result = client.post('/api/v1/meals/add',
                         data={
                             'trip_id': 1,
                             'meal_name': 0,
                             'day_number': 1,
                             'mass': 10,
                             'unit': 'grams',
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
                                         'unit': 'grams',
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
                                        'unit': 'grams',
                                        'product_id': 1
                                    })
    assert result.status_code == 200


def test_api_add_adds_a_product_successfully(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 987,
                                        'unit': 'grams',
                                        'product_id': 5
                                    })

    assert result.json['result']
    result = org_logged_client.get('/meals/1')
    assert b'987' in result.data
    assert b'Borsch concentrate' in result.data


def test_api_add_merges_existing_product(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 442,
                                        'unit': 'grams',
                                        'product_id': 1
                                    })

    assert result.json['result']
    result = org_logged_client.get('/meals/1')
    assert b'502' in result.data # 442 + existing 60 for multigrain cereal


def test_api_add_adds_a_product_with_pcs(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
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

    result = org_logged_client.post('/api/v1/meals/add',
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


def test_api_add_returns_fail_on_incorrect_trip_id(org_logged_client):
    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 'not a number',
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': 'grams',
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 982,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': 'grams',
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
                                        'unit': 'grams',
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'nan',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': 'grams',
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
                                        'unit': 'grams',
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 'nan',
                                        'mass': 10,
                                        'unit': 'grams',
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
                                        'unit': 'grams',
                                        'product_id': 1
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 'nan',
                                        'unit': 'grams',
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
                                        'unit': 'pcs',
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
                                        'unit': 'grams',
                                        'product_id': 487
                                    })
    assert not result.json['result']

    result = org_logged_client.post('/api/v1/meals/add',
                                    data={
                                        'trip_id': 1,
                                        'meal_name': 'breakfast',
                                        'day_number': 1,
                                        'mass': 10,
                                        'unit': 'grams',
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
                                        'unit': 'grams',
                                        'product_id': 15
                                    })
    assert not result.json['result']


def test_api_remove_uses_correct_method(org_logged_client):
    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={
                                          'meal_id': 1
                                      })
    assert result.status_code == 200


def test_api_remove_removes_meal_record(org_logged_client):
    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={
                                          'meal_id': 1
                                      })
    assert result.json['result']


def test_api_remove_returns_fail_on_incorrect_meal_id(org_logged_client):
    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={'meal_id': -900})
    assert not result.json['result']

    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={'meal_id': 900})
    assert not result.json['result']

    result = org_logged_client.delete('/api/v1/meals/remove',
                                      data={'meal_id': 'nan'})
    assert not result.json['result']
