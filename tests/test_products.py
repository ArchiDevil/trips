from flask.testing import FlaskClient

import pytest
from organizer.db import get_session
from organizer.schema import Product
from organizer.strings import STRING_TABLE


def test_index_page_rejects_not_logged_in(client):
    result = client.get('/products/')
    assert 'auth/login' in result.location
    assert result.status_code == 302  # redirect to auth page


def test_index_page_shows_products(org_logged_client: FlaskClient):
    result = org_logged_client.get('/products/')
    assert result.status_code == 200


def test_add_page_rejects_not_logged_in(client):
    result = client.post('/products/add')
    assert 'auth/login' in result.location
    assert result.status_code == 302  # redirect to auth page


def test_add_page_uses_correct_method(org_logged_client):
    result = org_logged_client.get('/products/add',
                                   data={
                                       'name': '',
                                       'calories': '',
                                       'proteins': '',
                                       'fats': '',
                                       'carbs': ''
                                   })
    assert result.status_code == 405


def test_add_page_redirects_after_add(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '21.2',
                                        'proteins': '4.0',
                                        'fats': '5.1',
                                        'carbs': '1.1'
                                    })
    assert 'products' in result.location
    assert result.status_code == 302


def test_add_page_adds_product(org_logged_client, app):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '21.2',
                                        'proteins': '4.0',
                                        'fats': '5.1',
                                        'carbs': '1.1'
                                    })
    assert result.status_code == 302

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 21.2
            assert prod.proteins == 4.0
            assert prod.fats == 5.1
            assert prod.carbs == 1.1


def test_add_page_adds_product_with_grams(org_logged_client, app):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '21.2',
                                        'proteins': '4.0',
                                        'fats': '5.1',
                                        'carbs': '1.1',
                                        'grams': '14.4'
                                    })
    assert result.status_code == 302

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 21.2
            assert prod.proteins == 4.0
            assert prod.fats == 5.1
            assert prod.carbs == 1.1
            assert prod.grams == 14.4


def test_add_page_redirects_after_adding(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    headers=[('Referer', '/chaoticgods')],
                                    data={
                                        'name': 'Test product',
                                        'calories': '21.2',
                                        'proteins': '4.0',
                                        'fats': '5.1',
                                        'carbs': '1.1',
                                        'grams': '14.4'
                                    })
    assert result.status_code == 302
    assert '/chaoticgods' in result.location


@pytest.mark.parametrize('name', ['', 'a'*101])
def test_add_page_rejects_incorrect_name(org_logged_client, app, name: str):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': name,
                                        'calories': '21.8',
                                        'proteins': '4.9',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect name'].encode() in result.data

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == name).first()
            assert not prod


@pytest.mark.parametrize('cals', ['-71.9', 'nan'])
def test_add_page_rejects_incorrect_cals(org_logged_client, app, cals: str):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': cals,
                                        'proteins': '4.9',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect calories'].encode(
    ) in result.data

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('prots', ['-71.9', 'nan', '171.9'])
def test_add_page_rejects_incorrect_proteins(org_logged_client, app, prots: str):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': prots,
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect proteins'].encode(
    ) in result.data

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('fats', ['-71.9', 'nan', '171.9'])
def test_add_page_rejects_incorrect_fats(org_logged_client, app, fats: str):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': fats,
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect fats'].encode(
    ) in result.data

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('carbs', ['-71.9', 'nan', '171.9'])
def test_add_page_rejects_incorrect_carbs(org_logged_client, app, carbs: str):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': '19.9',
                                        'carbs': carbs
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect carbs'].encode(
    ) in result.data

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('grams', ['-71.9', 'nan'])
def test_add_page_rejects_incorrect_grams(org_logged_client, app, grams: str):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '19.9',
                                        'fats': '5.6',
                                        'carbs': '17.1',
                                        'grams': grams
                                    })
    # TODO: there is no way to understand was it added or not
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect grams'].encode(
    ) in result.data

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


def test_archive_page_rejects_not_logged_in(client):
    result = client.get('/products/archive/1')
    assert 'auth/login' in result.location
    assert result.status_code == 302  # redirect to auth page


def test_archive_page_rejects_users(org_logged_client):
    result = org_logged_client.get('/products/archive/1')
    assert result.status_code == 403


def test_archive_page_uses_correct_method(admin_logged_client):
    result = admin_logged_client.get('/products/archive/1')
    assert 'products' in result.location
    assert result.status_code == 302  # redirect to index


def test_archive_page_returns_404_for_non_existing_product(admin_logged_client):
    result = admin_logged_client.get('/products/archive/100500')
    assert result.status_code == 404


def test_archive_page_archives_product(admin_logged_client, app):
    result = admin_logged_client.get('/products/archive/2')
    assert result.status_code == 302

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.archived


def test_archive_page_redirects_to_the_same_page(admin_logged_client):
    result = admin_logged_client.get('/products/archive/2',
                                     headers=[('Referer', '/chaoticgods')])
    assert result.status_code == 302
    assert '/chaoticgods' in result.location


def test_edit_rejects_not_logged_in(client):
    result = client.post('/products/edit/1',
                         data={
                             'name': 'Test product',
                             'calories': '249.6',
                             'proteins': '16.6',
                             'fats': '71.9',
                             'carbs': '41.9'
                         })
    assert 'auth/login' in result.location
    assert result.status_code == 302


def test_edit_page_rejects_users(org_logged_client):
    result = org_logged_client.post('/products/edit/1',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    assert result.status_code == 403


def test_edit_page_uses_correct_method(org_logged_client):
    result = org_logged_client.get('/products/edit/1',
                                   data={
                                       'name': 'Test product',
                                       'calories': '249.6',
                                       'proteins': '16.6',
                                       'fats': '71.9',
                                       'carbs': '41.9'
                                   })
    assert result.status_code == 405


def test_edit_page_redirects_after_edit(admin_logged_client):
    result = admin_logged_client.post('/products/edit/1',
                                      data={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9'
                                      })
    assert result.status_code == 302
    assert 'products' in result.location


def test_edit_page_edits(admin_logged_client, app):
    result = admin_logged_client.post('/products/edit/1',
                                      data={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9'
                                      })
    assert result.status_code == 302

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 249.6
            assert prod.proteins == 16.6
            assert prod.fats == 71.9
            assert prod.carbs == 41.9


def test_edit_page_edits_with_grams(admin_logged_client, app):
    result = admin_logged_client.post('/products/edit/1',
                                      data={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9',
                                          'grams': '250.0'
                                      })
    assert result.status_code == 302

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').one()
            assert prod.calories == 249.6
            assert prod.proteins == 16.6
            assert prod.fats == 71.9
            assert prod.carbs == 41.9
            assert prod.grams == 250.0


def test_edit_page_redirects_after_editing(admin_logged_client):
    result = admin_logged_client.post('/products/edit/1',
                                      headers=[('Referer', '/chaoticgods')],
                                      data={
                                          'name': 'Test product',
                                          'calories': '21.2',
                                          'proteins': '4.0',
                                          'fats': '5.1',
                                          'carbs': '1.1',
                                          'grams': '14.4'
                                      })
    assert result.status_code == 302
    assert '/chaoticgods' in result.location


@pytest.mark.parametrize('name', ['', 'a'*101])
def test_edit_page_rejects_incorrect_name(org_logged_client, app, name: str):
    org_logged_client.post('/products/edit/2',
                           data={
                               'name': name,
                               'calories': '249.6',
                               'proteins': '16.6',
                               'fats': '71.9',
                               'carbs': '41.9'
                           })

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.calories != 249.6
            assert prod.proteins != 16.6
            assert prod.fats != 71.9
            assert prod.carbs != 41.9


@pytest.mark.parametrize('cals', ['-71.9', 'nan'])
def test_edit_page_rejects_incorrect_cals(org_logged_client, app, cals: str):
    org_logged_client.post('/products/edit/2',
                           data={
                               'name': 'Test product',
                               'calories': cals,
                               'proteins': '16.6',
                               'fats': '71.9',
                               'carbs': '41.9'
                           })

    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.calories != 249.6
            assert prod.proteins != 16.6
            assert prod.fats != 71.9
            assert prod.carbs != 41.9

            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('prots', ['-71.9', 'nan', '171.9'])
def test_edit_page_rejects_incorrect_proteins(org_logged_client, app, prots: str):
    org_logged_client.post('/products/edit/2',
                           data={
                               'name': 'Test product',
                               'calories': '249.6',
                               'proteins': prots,
                               'fats': '71.9',
                               'carbs': '41.9'
                           })
    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.calories != 249.6
            assert prod.proteins != 16.6
            assert prod.fats != 71.9
            assert prod.carbs != 41.9

            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('fats', ['-71.9', 'nan', '171.9'])
def test_edit_page_rejects_incorrect_fats(org_logged_client, app, fats: str):
    org_logged_client.post('/products/edit/2',
                           data={
                               'name': 'Test product',
                               'calories': '249.6',
                               'proteins': '16.6',
                               'fats': fats,
                               'carbs': '41.9'
                           })
    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.calories != 249.6
            assert prod.proteins != 16.6
            assert prod.fats != 71.9
            assert prod.carbs != 41.9

            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('carbs', ['-71.9', 'nan', '171.9'])
def test_edit_page_rejects_incorrect_carbs(org_logged_client, app, carbs: str):
    org_logged_client.post('/products/edit/2',
                           data={
                               'name': 'Test product',
                               'calories': '249.6',
                               'proteins': '16.6',
                               'fats': '71.9',
                               'carbs': carbs
                           })
    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.calories != 249.6
            assert prod.proteins != 16.6
            assert prod.fats != 71.9
            assert prod.carbs != 41.9

            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


@pytest.mark.parametrize('grams', ['-71.9', 'nan'])
def test_edit_page_rejects_incorrect_grams(org_logged_client, app, grams: str):
    org_logged_client.post('/products/edit/2',
                           data={
                               'name': 'Test product',
                               'calories': '-249.6',
                               'proteins': '16.6',
                               'fats': '71.9',
                               'carbs': '41.9',
                               'grams': grams
                           })
    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(Product.name == 'Mango').one()
            assert prod.calories != 249.6
            assert prod.proteins != 16.6
            assert prod.fats != 71.9
            assert prod.carbs != 41.9

            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod


def test_edit_page_returns_404_for_non_existing_product(admin_logged_client, app):
    result = admin_logged_client.post('/products/edit/200',
                                      data={
                                          'name': 'Test product',
                                          'calories': '249.6',
                                          'proteins': '16.6',
                                          'fats': '71.9',
                                          'carbs': '41.9'
                                      })
    assert result.status_code == 404
    with app.app_context():
        with get_session() as session:
            prod = session.query(Product).filter(
                Product.name == 'Test product').first()
            assert not prod
