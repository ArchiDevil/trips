import pytest

from flask.testing import FlaskClient

from organizer.db import get_session
from organizer.schema import Product, Units
from organizer.strings import STRING_TABLE


def test_api_search_rejects_not_logged_in(client: FlaskClient):
    result = client.get('/api/products/search',
                        query_string={
                            'search': 'Mango'
                        })
    assert result.status_code == 401


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
    assert result.status_code == 401


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


def test_api_search_does_not_show_archived(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                   query_string={'search': ''})
    assert result.status_code == 200
    assert result.json
    for product in result.json['products']:
        assert product['name'] != 'Archived'


def test_api_search_change_pages(org_logged_client: FlaskClient):
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


def test_api_search_searches(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/search',
                                    query_string={'search': 'jerk'})
    assert result.status_code == 200
    assert result.json
    for product in result.json['products']:
        assert product['name'] != 'Mango'
    assert any(map(lambda x: 'jerk' in x['name'], result.json['products']))


def test_api_add_rejects_not_logged_in(client: FlaskClient):
    result = client.post('/api/products/add')
    assert result.status_code == 401


def test_api_add_uses_correct_method(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/add',
                                   data={
                                       'name': '',
                                       'calories': '',
                                       'proteins': '',
                                       'fats': '',
                                       'carbs': ''
                                   })
    assert result.status_code == 405


def test_api_add_adds_product(org_logged_client: FlaskClient):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': 'Test product',
                                        'calories': '21.2',
                                        'proteins': '4.0',
                                        'fats': '5.1',
                                        'carbs': '1.1'
                                    })
    assert result.status_code == 200
    assert result.json
    assert result.json['result'] == True

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 21.2
            assert prod.proteins == 4.0
            assert prod.fats == 5.1
            assert prod.carbs == 1.1


def test_api_add_adds_product_with_grams(org_logged_client: FlaskClient):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': 'Test product',
                                        'calories': '21.2',
                                        'proteins': '4.0',
                                        'fats': '5.1',
                                        'carbs': '1.1',
                                        'grams': '14.4'
                                    })
    assert result.status_code == 200
    assert result.json
    assert result.json['result'] == True

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 21.2
            assert prod.proteins == 4.0
            assert prod.fats == 5.1
            assert prod.carbs == 1.1
            assert prod.grams == 14.4


def test_api_add_rejects_no_data(org_logged_client: FlaskClient):
    result = org_logged_client.post('/api/products/add', json={})
    assert result.status_code == 400


@pytest.mark.parametrize('name', ['', 'a'*101])
def test_api_add_rejects_incorrect_name(org_logged_client: FlaskClient, name: str):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': name,
                                        'calories': '21.8',
                                        'proteins': '4.9',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    assert result.status_code == 200
    assert result.json
    assert not result.json['result']
    assert STRING_TABLE['Products error incorrect name'] in result.json['error']

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == name).first()
            assert not prod


@pytest.mark.parametrize('cals', ['-71.9', 'nan'])
def test_api_add_rejects_incorrect_cals(org_logged_client: FlaskClient, cals: str):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': 'Test product',
                                        'calories': cals,
                                        'proteins': '4.9',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    assert result.status_code == 200
    assert result.json
    assert not result.json['result']
    assert STRING_TABLE['Products error incorrect calories'] in result.json['error']

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('prots', ['-71.9', 'nan', '171.9'])
def test_api_add_rejects_incorrect_proteins(org_logged_client: FlaskClient, prots: str):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': prots,
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    assert result.status_code == 200
    assert result.json
    assert not result.json['result']
    assert STRING_TABLE['Products error incorrect proteins'] in result.json['error']

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('fats', ['-71.9', 'nan', '171.9'])
def test_api_add_rejects_incorrect_fats(org_logged_client: FlaskClient, fats: str):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': fats,
                                        'carbs': '19.9'
                                    })
    assert result.status_code == 200
    assert result.json
    assert not result.json['result']
    assert STRING_TABLE['Products error incorrect fats'] in result.json['error']

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('carbs', ['-71.9', 'nan', '171.9'])
def test_api_add_rejects_incorrect_carbs(org_logged_client: FlaskClient, carbs: str):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': '19.9',
                                        'carbs': carbs
                                    })
    assert result.status_code == 200
    assert result.json
    assert not result.json['result']
    assert STRING_TABLE['Products error incorrect carbs'] in result.json['error']

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('grams', ['-71.9', 'nan'])
def test_api_add_rejects_incorrect_grams(org_logged_client: FlaskClient, grams: str):
    result = org_logged_client.post('/api/products/add',
                                    json={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '19.9',
                                        'fats': '5.6',
                                        'carbs': '17.1',
                                        'grams': grams
                                    })
    assert result.status_code == 200
    assert result.json
    assert not result.json['result']
    assert STRING_TABLE['Products error incorrect grams'] in result.json['error']

    with org_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


def test_api_edit_rejects_not_logged_in(client: FlaskClient):
    result = client.post('/api/products/1/edit',
                         json={
                             'name': 'Test product',
                             'calories': '249.6',
                             'proteins': '16.6',
                             'fats': '71.9',
                             'carbs': '41.9'
                         })
    assert result.status_code == 401


def test_api_edit_rejects_users(org_logged_client: FlaskClient):
    result = org_logged_client.post('/api/products/1/edit',
                                    json={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    assert result.status_code == 403


def test_api_edit_uses_correct_method(org_logged_client: FlaskClient):
    result = org_logged_client.get('/api/products/1/edit',
                                   json={
                                       'name': 'Test product',
                                       'calories': '249.6',
                                       'proteins': '16.6',
                                       'fats': '71.9',
                                       'carbs': '41.9'
                                   })
    assert result.status_code == 405


def test_api_edit_redirects_after_edit(admin_logged_client: FlaskClient):
    result = admin_logged_client.post('/api/products/1/edit',
                                      json={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9'
                                      })
    assert result.status_code == 200
    assert result.json
    assert result.json['result']


def test_api_edit_edits(admin_logged_client: FlaskClient):
    result = admin_logged_client.post('/api/products/1/edit',
                                      json={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9'
                                      })
    assert result.status_code == 200
    assert result.json
    assert result.json['result']

    with admin_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 249.6
            assert prod.proteins == 16.6
            assert prod.fats == 71.9
            assert prod.carbs == 41.9


def test_api_edit_edits_with_grams(admin_logged_client: FlaskClient):
    result = admin_logged_client.post('/api/products/1/edit',
                                      json={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9',
                                          'grams': '250.0'
                                      })
    assert result.status_code == 200
    assert result.json
    assert result.json['result']

    with admin_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 249.6
            assert prod.proteins == 16.6
            assert prod.fats == 71.9
            assert prod.carbs == 41.9
            assert prod.grams == 250.0


def test_api_edit_rejects_no_data(admin_logged_client: FlaskClient):
    result = admin_logged_client.post('/api/products/1/edit', json={})
    assert result.status_code == 400


@pytest.mark.parametrize('test_data', [
    {'name': ''},
    {'name': 'a'*101},
    {'calories': '-71.9'},
    {'calories': 'nan'},
    {'proteins': '-71.9'},
    {'proteins': 'nan'},
    {'proteins': '171.9'},
    {'fats': '-71.9'},
    {'fats': 'nan'},
    {'fats': '171.9'},
    {'carbs': '-71.9'},
    {'carbs': 'nan'},
    {'carbs': '171.9'},
    {'grams': '-71.9'},
    {'grams': 'nan'},
])
def test_api_edit_rejects_incorrect_data(admin_logged_client: FlaskClient,
                                         test_data: dict):
    input_data = {
        'name': 'Test product',
        'calories': '249.6',
        'proteins': '16.6',
        'fats': '71.9',
        'carbs': '41.9'
    }
    input_data.update(test_data)

    result = admin_logged_client.post('/api/products/2/edit', json=input_data)

    assert result.status_code == 200
    assert result.json
    assert not result.json['result']

    with admin_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.calories != 249.6
            assert prod.proteins != 16.6
            assert prod.fats != 71.9
            assert prod.carbs != 41.9


def test_api_edit_returns_404_for_non_existing_product(admin_logged_client: FlaskClient):
    result = admin_logged_client.post('/api/products/200/edit',
                                      json={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9'
                                      })
    assert result.status_code == 404
    with admin_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


def test_api_archive_rejects_not_logged_in(client: FlaskClient):
    result = client.post('/api/products/1/archive')
    assert result.status_code == 401


def test_api_archive_rejects_users(org_logged_client: FlaskClient):
    result = org_logged_client.post('/api/products/1/archive')
    assert result.status_code == 403


def test_api_archive_uses_correct_method(admin_logged_client: FlaskClient):
    result = admin_logged_client.get('/api/products/1/archive')
    assert result.status_code == 405


def test_api_archive_returns_404_for_non_existing_product(admin_logged_client: FlaskClient):
    result = admin_logged_client.post('/api/products/100500/archive')
    assert result.status_code == 404


def test_api_archive_archives_product(admin_logged_client: FlaskClient):
    result = admin_logged_client.post('/api/products/2/archive')

    assert result.status_code == 200
    assert result.json
    assert result.json['result']

    with admin_logged_client.application.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.archived
