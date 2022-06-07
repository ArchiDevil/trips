import pytest

from flask.testing import FlaskClient

from organizer.schema import Units


def test_api_search_rejects_not_logged_in(client: FlaskClient):
    result = client.get('/api/products/search',
                        query_string={
                            'search': 'Mango'
                        })
    assert result.status_code == 403


def test_api_search_uses_correct_method(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                   query_string={
                                       'search': 'Mango'
                                   })
    assert result.status_code == 200


def test_api_search_does_not_find_archived(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                   query_string={
                                       'search': 'Archived'
                                   })
    assert result.json
    assert not result.json['products']


def test_api_search_does_not_fail_with_incorrect_name(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                   query_string={
                                       'search': '%;DROP TABLE products;'
                                   })
    assert result.status_code == 200
    assert result.json
    assert not result.json['products']


def test_api_units_uses_correct_method(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/units',
                                    query_string={'id': 2})
    assert result.status_code == 200


def test_api_units_rejects_not_logged_in(client: FlaskClient):
    result = client.get('/api/products/units',
                        query_string={'id': 9})
    assert result.status_code == 403


def test_api_units_return_units(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/units',
                                   query_string={'id': 2})
    assert result.json
    assert result.json['result']
    assert result.json['units'] == [Units.GRAMMS.value]


def test_api_units_return_multi_units(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/units',
                                   query_string={'id': 9})
    assert result.json
    assert result.json['result']
    assert result.json['units'] == [Units.GRAMMS.value, Units.PIECES.value]


def test_api_units_return_nothing_on_archived(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/units',
                                   query_string={'id': 15})
    assert result.json
    assert not result.json['result']


@pytest.mark.parametrize('id', ['not even a number', -200])
def test_api_units_fails_on_incorrect_id(org_logged_client: FlaskClient, id: str | int):
    result = org_logged_client.get('/api/products/units',
                                   query_string={'id': id})
    assert result.json
    assert not result.json['result']


def test_index_page_does_not_show_archived(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                   query_string={'search': ''})
    assert result.status_code == 200
    assert result.json
    for product in result.json['products']:
        assert product['name'] != 'Archived'


def test_index_page_change_pages(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                    query_string={'page': 0})
    assert result.status_code == 200
    assert result.json
    for product in result.json['products']:
        assert product['name'] not in ['Sausage', 'Chocolate', 'Step snack']

    result = org_logged_client.get('/api/products/search',
                                    query_string={'page': 1})
    assert result.status_code == 200
    assert result.json
    for product in result.json['products']:
        assert product['name'] not in ['Multigrain cereal', 'Mango', 'Cream cheese']


def test_index_page_searches(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                    query_string={'search': 'jerk'})
    assert result.status_code == 200
    assert result.json
    for product in result.json['products']:
        assert product['name'] != 'Mango'
    assert any(map(lambda x: 'jerk' in x['name'], result.json['products']))
