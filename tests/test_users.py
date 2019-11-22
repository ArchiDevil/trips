def test_users_rejects_not_logged_in(client):
    response = client.get('/users/')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_users_rejects_guests(user_logged_client):
    response = user_logged_client.get('/users/')
    assert response.status_code == 403


def test_users_rejects_trip_managers(org_logged_client):
    response = org_logged_client.get('/users/')
    assert response.status_code == 403


def test_users_shows_users(admin_logged_client):
    response = admin_logged_client.get('/users/')
    assert response.status_code == 200
    assert b'User' in response.data
    assert b'Organizer' in response.data
    assert b'Administrator' in response.data


def test_users_add_rejects_not_logged_in(client):
    response = client.get('/users/add')
    assert response.status_code == 302
    assert '/auth/login' in response.location

    response = client.post('/users/add',
                           data={
                               'name': 'test',
                               'password': '123',
                               'group': 'Guest'
                           })
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_users_add_rejects_guests(user_logged_client):
    response = user_logged_client.get('/users/add')
    assert response.status_code == 403

    response = user_logged_client.post('/users/add',
                                       data={
                                           'name': 'test',
                                           'password': '123',
                                           'group': 'Guest'
                                       })
    assert response.status_code == 403


def test_users_add_rejects_trip_managers(org_logged_client):
    response = org_logged_client.get('/users/add')
    assert response.status_code == 403

    response = org_logged_client.post('/users/add',
                                      data={
                                          'name': 'test',
                                          'password': '123',
                                          'group': 'Guest'
                                      })
    assert response.status_code == 403


def test_users_add_shows_page(admin_logged_client):
    response = admin_logged_client.get('/users/add')
    assert response.status_code == 200


def test_users_add_adds_user(admin_logged_client):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'name': 'Test user',
                                            'password': '123',
                                            'group': 'TripManager'
                                        })
    assert response.status_code == 302
    assert '/users/' in response.location

    response = admin_logged_client.get('/users/')
    assert b'Test user' in response.data


def test_users_add_rejects_empty_name(admin_logged_client):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'name': '',
                                            'password': '123',
                                            'group': 'TripManager'
                                        })
    assert response.status_code == 200
    assert b'Empty name provided' in response.data


def test_users_add_rejects_empty_password(admin_logged_client):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'name': 'Test user',
                                            'password': '',
                                            'group': 'TripManager'
                                        })
    assert response.status_code == 200
    assert b'Empty password provided' in response.data

    response = admin_logged_client.get('/users/')
    assert b'Test user' not in response.data


def test_users_add_rejects_empty_group(admin_logged_client):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'name': 'Test user',
                                            'password': '123',
                                            'group': ''
                                        })
    assert response.status_code == 200
    assert b'Empty group provided' in response.data

    response = admin_logged_client.get('/users/')
    assert b'Test user' not in response.data


def test_users_add_rejects_wrong_group(admin_logged_client):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'name': 'Test user',
                                            'password': '123',
                                            'group': 'WRONG'
                                        })
    assert response.status_code == 200
    assert b'Wrong group provided' in response.data

    response = admin_logged_client.get('/users/')
    assert b'Test user' not in response.data


def test_users_remove_rejects_not_logged_in(client):
    response = client.get('/users/remove/2')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_users_remove_rejects_guests(user_logged_client):
    response = user_logged_client.get('/users/remove/2')
    assert response.status_code == 403


def test_users_remove_rejects_trip_managers(org_logged_client):
    response = org_logged_client.get('/users/remove/2')
    assert response.status_code == 403


def test_users_remove_removes_user(admin_logged_client):
    response = admin_logged_client.get('/users/remove/2')
    assert response.status_code == 302
    assert '/users/' in response.location

    response = admin_logged_client.get('/users/')
    assert b'Organizer' not in response.data


def test_users_remove_returns_404_on_wrong_user(admin_logged_client):
    response = admin_logged_client.get('/users/remove/1000')
    assert response.status_code == 404


def test_users_remove_cannot_remove_current_user(admin_logged_client):
    response = admin_logged_client.get('/users/remove/1')
    assert response.status_code == 403 # forbidden to remove current user
