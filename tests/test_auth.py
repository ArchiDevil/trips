def test_auth_can_see_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_auth_can_log_in_as_user(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'Administrator',
                               'password': 'qwerty'
                           })
    assert client.cookie_jar
    for x in client.cookie_jar:
        assert not x.expires

    assert response.status_code == 302
    assert '/' in response.location


def test_auth_can_log_in_as_user_with_remember(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'Administrator',
                               'password': 'qwerty',
                               'remember': 'true'
                           })
    assert client.cookie_jar
    for x in client.cookie_jar:
        assert x.expires

    assert response.status_code == 302
    assert '/' in response.location


def test_auth_reports_login_error(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'No no no',
                               'password': 'qwerty'
                           })
    assert response.status_code == 200
    assert b'No such user'


def test_auth_reports_password_error(client):
    response = client.post('/auth/login',
                           data={
                               'login': 'Administrator',
                               'password': 'invalid pass'
                           })
    assert response.status_code == 200
    assert b'Incorrect password'


def test_auth_logout_requires_login(client):
    response = client.get('/auth/logout')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_auth_can_logout(user_logged_client):
    response = user_logged_client.get('/auth/logout')
    assert not user_logged_client.cookie_jar
    assert response.status_code == 302
    assert '/' in response.location
