def test_api_search_uses_correct_method(client):
    result = client.get('/api/v1/products/search',
                        query_string={
                            'name': 'Mango',
                            'count': 10
                        })
    assert result.status_code == 200


def test_api_search_finds_element(client):
    result = client.get('/api/v1/products/search',
                        query_string={
                            'name': 'Mango',
                            'count': 10
                        })
    assert result.json['result']
    assert len(result.json['products']) == 1
    assert result.json['products'][0]['id'] == 2
    assert result.json['products'][0]['name'] == 'Mango'


def test_api_search_returns_no_more_than_count(client):
    result = client.get('/api/v1/products/search',
                        query_string={
                            'name': '',
                            'count': 5
                        })
    assert len(result.json['products']) == 5


def test_api_search_does_not_find_archived(client):
    result = client.get('/api/v1/products/search',
                        query_string={
                            'name': 'Archived',
                            'count': 1
                        })
    assert not result.json['products']


def test_api_search_does_not_fail_with_incorrect_name(client):
    result = client.get('/api/v1/products/search',
                        query_string={
                            'name': '%;DROP TABLE products;',
                            'count': ''
                        })
    assert result.json == {'result': False}


def test_api_search_reacts_to_incorrect_count(client):
    result = client.get('/api/v1/products/search',
                        query_string={
                            'name': '',
                            'count': 'Not a number'
                        })
    assert result.json == {'result': False}


def test_api_units_uses_correct_method(client):
    result = client.get('/api/v1/products/units',
                        query_string={'id': 2})
    assert result.status_code == 200


def test_api_units_return_units(client):
    result = client.get('/api/v1/products/units',
                        query_string={'id': 2})
    assert result.json['result']
    assert result.json['units'] == ['grams']


def test_api_units_return_multi_units(client):
    result = client.get('/api/v1/products/units',
                        query_string={'id': 9})
    assert result.json['result']
    assert result.json['units'] == ['grams', 'pcs']


def test_api_units_return_nothing_on_archived(client):
    result = client.get('/api/v1/products/units',
                        query_string={'id': 15})
    assert not result.json['result']


def test_api_units_fails_on_incorrect_id(client):
    result = client.get('/api/v1/products/units',
                        query_string={'id': 'not even a number'})
    assert not result.json['result']


def test_api_units_fails_on_unknown_id(client):
    result = client.get('/api/v1/products/units',
                        query_string={'id': -200})
    assert not result.json['result']
