from organizer.api import Units

def test_api_search_rejects_not_logged_in(client):
    result = client.get('/api/v1/products/search',
                        query_string={
                            'name': 'Mango',
                            'count': 10
                        })
    assert result.status_code == 403


def test_api_units_rejects_not_logged_in(client):
    result = client.get('/api/v1/products/units',
                        query_string={'id': 9})
    assert result.status_code == 403


def test_api_search_uses_correct_method(user_logged_client):
    result = user_logged_client.get('/api/v1/products/search',
                                    query_string={
                                        'name': 'Mango',
                                        'count': 10
                                    })
    assert result.status_code == 200


def test_api_search_finds_element(user_logged_client):
    result = user_logged_client.get('/api/v1/products/search',
                                    query_string={
                                        'name': 'Mango',
                                        'count': 10
                                    })
    assert result.json['result']
    assert len(result.json['products']) == 1
    assert result.json['products'][0]['id'] == 2
    assert result.json['products'][0]['name'] == 'Mango'


def test_api_search_returns_no_more_than_count(user_logged_client):
    result = user_logged_client.get('/api/v1/products/search',
                                    query_string={
                                        'name': '',
                                        'count': 5
                                    })
    assert len(result.json['products']) == 5


def test_api_search_does_not_find_archived(user_logged_client):
    result = user_logged_client.get('/api/v1/products/search',
                                    query_string={
                                        'name': 'Archived',
                                        'count': 1
                                    })
    assert not result.json['products']


def test_api_search_does_not_fail_with_incorrect_name(user_logged_client):
    result = user_logged_client.get('/api/v1/products/search',
                                    query_string={
                                        'name': '%;DROP TABLE products;',
                                        'count': ''
                                    })
    assert result.json == {'result': False}


def test_api_search_reacts_to_incorrect_count(user_logged_client):
    result = user_logged_client.get('/api/v1/products/search',
                                    query_string={
                                        'name': '',
                                        'count': 'Not a number'
                                    })
    assert result.json == {'result': False}


def test_api_units_uses_correct_method(user_logged_client):
    result = user_logged_client.get('/api/v1/products/units',
                                    query_string={'id': 2})
    assert result.status_code == 200


def test_api_units_return_units(user_logged_client):
    result = user_logged_client.get('/api/v1/products/units',
                                    query_string={'id': 2})
    assert result.json['result']
    assert result.json['units'] == [Units.Grams.value]


def test_api_units_return_multi_units(user_logged_client):
    result = user_logged_client.get('/api/v1/products/units',
                                    query_string={'id': 9})
    assert result.json['result']
    assert result.json['units'] == [Units.Grams.value, Units.Pieces.value]


def test_api_units_return_nothing_on_archived(user_logged_client):
    result = user_logged_client.get('/api/v1/products/units',
                                    query_string={'id': 15})
    assert not result.json['result']


def test_api_units_fails_on_incorrect_id(user_logged_client):
    result = user_logged_client.get('/api/v1/products/units',
                                    query_string={'id': 'not even a number'})
    assert not result.json['result']


def test_api_units_fails_on_unknown_id(user_logged_client):
    result = user_logged_client.get('/api/v1/products/units',
                                    query_string={'id': -200})
    assert not result.json['result']
