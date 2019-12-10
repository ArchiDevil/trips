from organizer.strings import STRING_TABLE

def test_index_page_rejects_not_logged_in(client):
    result = client.get('/products/')
    assert 'auth/login' in result.location
    assert result.status_code == 302  # redirect to auth page


def test_index_page_shows_products(user_logged_client):
    result = user_logged_client.get('/products/')
    assert result.status_code == 200
    assert b'Multigrain cereal' in result.data
    assert b'Mango' in result.data
    assert b'Cream cheese' in result.data


def test_index_page_does_not_show_archived(user_logged_client):
    result = user_logged_client.get('/products/')
    assert b'Archived' not in result.data


def test_index_page_is_not_filtered(user_logged_client):
    result = user_logged_client.get('/products/')
    assert STRING_TABLE['Products search notification'].encode() not in result.data


def test_index_page_change_pages(user_logged_client):
    result = user_logged_client.get('/products/?page=0')
    assert result.status_code == 200
    assert b'Multigrain cereal' in result.data
    assert b'Mango' in result.data
    assert b'Cream cheese' in result.data
    assert b'Sausage' not in result.data
    assert b'Chocolate' not in result.data
    assert b'Step snack' not in result.data

    result = user_logged_client.get('/products/?page=1')
    assert result.status_code == 200
    assert b'Multigrain cereal' not in result.data
    assert b'Mango' not in result.data
    assert b'Cream cheese' not in result.data
    assert b'Sausage' in result.data
    assert b'Chocolate' in result.data
    assert b'Step snack' in result.data


def test_index_page_searches(user_logged_client):
    result = user_logged_client.get('/products/?search=jerk')
    assert result.status_code == 200
    assert STRING_TABLE['Products search notification'].encode() in result.data
    assert b'jerk' in result.data
    assert b'Mango' not in result.data


def test_index_is_sql_injection_resistant(user_logged_client):
    result = user_logged_client.get('/products/?search="%;DROP TABLE products;"')
    assert result.status_code == 200
    assert STRING_TABLE['Products search notification'].encode() in result.data
    assert b'Mango' not in result.data


def test_index_page_change_pages_while_seaching(user_logged_client):
    result = user_logged_client.get('/products/?search=Mango&page=0')
    assert result.status_code == 200
    assert b'>Mango<' in result.data
    assert b'>Cream cheese<' not in result.data

    result = user_logged_client.get('/products/?search=Mango&page=1')
    assert result.status_code == 200
    assert b'>Mango<' not in result.data
    assert b'>Cream cheese<' not in result.data


def test_add_page_rejects_not_logged_in(client):
    result = client.post('/products/add')
    assert 'auth/login' in result.location
    assert result.status_code == 302  # redirect to auth page


def test_add_page_rejects_insufficient_privileges(user_logged_client):
    result = user_logged_client.post('/products/add')
    assert result.status_code == 403


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


def test_add_page_adds_product(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '21.2',
                                        'proteins': '4.0',
                                        'fats': '5.1',
                                        'carbs': '1.1'
                                    })
    result = org_logged_client.get('/products/?search=product')
    assert b'Test product' in result.data
    assert b'21.2' in result.data
    assert b'4.0' in result.data
    assert b'5.1' in result.data
    assert b'1.1' in result.data


def test_add_page_adds_product_with_grams(org_logged_client):
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

    # TODO: there is no way to understand was it added or not
    result = org_logged_client.get('/products/?search=product')
    assert b'Test product' in result.data
    assert b'21.2' in result.data
    assert b'4.0' in result.data
    assert b'5.1' in result.data
    assert b'1.1' in result.data


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


def test_add_page_reacts_to_incorrect_name(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': '',
                                        'calories': '21.8',
                                        'proteins': '4.9',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect name'].encode() in result.data
    assert b'21.8' not in result.data
    assert b'4.9' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_negative_cals(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '-900',
                                        'proteins': '4.9',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect calories'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'4.9' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_nan_cals(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': 'nan',
                                        'proteins': '4.9',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect calories'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'4.9' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_negative_proteins(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '-10.0',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect proteins'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_nan_proteins(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': 'nan',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect proteins'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_much_proteins(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '101.4',
                                        'fats': '5.6',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect proteins'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'101.4' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_negative_fats(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': '-10.0',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect fats'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_nan_fats(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': 'nan',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect fats'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_much_fats(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': '101.4',
                                        'carbs': '19.9'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect fats'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'101.4' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_negative_carbs(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '5.6',
                                        'fats': '19.9',
                                        'carbs': '-10.0'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect carbs'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_nan_carbs(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '19.9',
                                        'fats': '5.6',
                                        'carbs': 'nan'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect carbs'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_much_carbs(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '19.9',
                                        'fats': '5.6',
                                        'carbs': '101.4'
                                    })
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect carbs'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'101.4' not in result.data
    assert b'120.0' not in result.data
    assert b'5.6' not in result.data
    assert b'19.9' not in result.data


def test_add_page_reacts_to_negative_grams(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '19.9',
                                        'fats': '5.6',
                                        'carbs': '17.1',
                                        'grams': '-56.0'
                                    })
    # TODO: there is no way to understand was it added or not
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect grams'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'19.9' not in result.data
    assert b'5.6' not in result.data
    assert b'17.1' not in result.data


def test_add_page_reacts_to_nan_grams(org_logged_client):
    result = org_logged_client.post('/products/add',
                                    data={
                                        'name': 'Test product',
                                        'calories': '120.0',
                                        'proteins': '19.9',
                                        'fats': '5.6',
                                        'carbs': '17.1',
                                        'grams': 'nan'
                                    })
    # TODO: there is no way to understand was it added or not
    result = org_logged_client.get('/products/')
    assert STRING_TABLE['Products error incorrect grams'].encode() in result.data
    assert b'Test product' not in result.data
    assert b'120.0' not in result.data
    assert b'19.9' not in result.data
    assert b'5.6' not in result.data
    assert b'17.1' not in result.data


def test_archive_page_rejects_not_logged_in(client):
    result = client.get('/products/archive/1')
    assert 'auth/login' in result.location
    assert result.status_code == 302  # redirect to auth page


def test_archive_page_rejects_insufficient_privileges(user_logged_client):
    result = user_logged_client.get('/products/archive/1')
    assert result.status_code == 403


def test_archive_page_uses_correct_method(org_logged_client):
    result = org_logged_client.get('/products/archive/1')
    assert 'products' in result.location
    assert result.status_code == 302  # redirect to index


def test_archive_page_returns_404_for_non_existing_product(org_logged_client):
    result = org_logged_client.get('/products/archive/100500')
    assert result.status_code == 404


def test_archive_page_archives_product(org_logged_client):
    result = org_logged_client.get('/products/archive/2')
    assert result.status_code == 302

    result = org_logged_client.get('/products/')
    assert b'Mango' not in result.data


def test_archive_page_redirects_to_the_same_page(org_logged_client):
    result = org_logged_client.get('/products/archive/2', headers=[('Referer', '/chaoticgods')])
    assert result.status_code == 302
    assert '/chaoticgods' in result.location

    result = org_logged_client.get('/products/')
    assert b'Mango' not in result.data


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


def test_edit_rejects_insufficient_privileges(user_logged_client):
    result = user_logged_client.post('/products/edit/1',
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


def test_edit_page_redirects_after_edit(org_logged_client):
    result = org_logged_client.post('/products/edit/1',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    assert result.status_code == 302
    assert 'products' in result.location


def test_edit_page_edits(org_logged_client):
    result = org_logged_client.post('/products/edit/1',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Test product' in result.data
    assert b'249.6' in result.data
    assert b'16.6' in result.data
    assert b'71.9' in result.data
    assert b'41.9' in result.data


def test_edit_page_edits_with_grams(org_logged_client):
    result = org_logged_client.post('/products/edit/1',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9',
                                        'grams': '250.0'
                                    })
    assert result.status_code == 302

    result = org_logged_client.get('/products/')
    # TODO: there is no way to understand if grams were added or not :(
    assert b'Test product' in result.data
    assert b'249.6' in result.data
    assert b'16.6' in result.data
    assert b'71.9' in result.data
    assert b'41.9' in result.data


def test_edit_page_redirects_after_editing(org_logged_client):
    result = org_logged_client.post('/products/edit/1',
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


def test_edit_page_reacts_to_incorrect_name(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': '',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_negative_cals(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '-249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_nan_cals(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': 'nan',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_negative_proteins(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '-16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'-16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_nan_proteins(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': 'nan',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_much_proteins(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '116.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'116.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_negative_fats(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '-71.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'-71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_nan_fats(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': 'nan',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_much_fats(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '171.9',
                                        'carbs': '41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'171.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_negative_carbs(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '-41.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'-41.9' not in result.data


def test_edit_page_reacts_to_nan_carbs(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': 'nan'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data


def test_edit_page_reacts_to_much_carbs(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '141.9'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'141.9' not in result.data


def test_edit_page_reacts_to_negative_grams(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '-249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9',
                                        'grams': '-200.0'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_reacts_to_nan_grams(org_logged_client):
    result = org_logged_client.post('/products/edit/2',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9',
                                        'grams': 'nan'
                                    })
    result = org_logged_client.get('/products/')
    assert b'Mango' in result.data
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data


def test_edit_page_returns_404_for_non_existing_product(org_logged_client):
    result = org_logged_client.post('/products/edit/200',
                                    data={
                                        'name': 'Test product',
                                        'calories': '249.6',
                                        'proteins': '16.6',
                                        'fats': '71.9',
                                        'carbs': '41.9'
                                    })
    assert result.status_code == 404
    result = org_logged_client.get('/products/')
    assert b'Test product' not in result.data
    assert b'249.6' not in result.data
    assert b'16.6' not in result.data
    assert b'71.9' not in result.data
    assert b'41.9' not in result.data
