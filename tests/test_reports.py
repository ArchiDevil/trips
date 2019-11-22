# TODO: no tests check correctness of the data


def test_shopping_rejects_not_logged_in(client):
    response = client.get('/reports/shopping/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_shopping_shows_report(user_logged_client):
    response = user_logged_client.get('/reports/shopping/1')
    assert response.status_code == 200
    assert b'Taganay' in response.data
    assert b'Mango' in response.data
    assert b'pcs)' in response.data


def test_shopping_returns_404_on_invalid_trip_id(user_logged_client):
    response = user_logged_client.get('/reports/shopping/100')
    assert response.status_code == 404


def test_packing_rejects_not_logged_in(client):
    response = client.get('/reports/packing/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_packing_shows_report(user_logged_client):
    response = user_logged_client.get('/reports/packing/1')
    assert response.status_code == 302
    assert '/reports/packing/1' in response.location


def test_packing_custom_rejects_not_logged_in(client):
    response = client.get('/reports/packing/1/4')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_packing_custom_shows_report(user_logged_client):
    response = user_logged_client.get('/reports/packing/1/4')
    assert response.status_code == 200
    assert b'Taganay' in response.data
    assert b'Mango' in response.data


def test_packing_custom_returns_404_on_invalid_trip_id(user_logged_client):
    response = user_logged_client.get('/reports/packing/100/4')
    assert response.status_code == 404


def test_packing_custom_returns_403_on_invalid_columns_count(user_logged_client):
    response = user_logged_client.get('/reports/packing/1/7')
    assert response.status_code == 403
    response = user_logged_client.get('/reports/packing/1/0')
    assert response.status_code == 403
