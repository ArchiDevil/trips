def test_developer_requires_log_in(client):
    response = client.get('/developer/console')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_developer_requires_admin_user(org_logged_client):
    response = org_logged_client.get('/developer/console')
    assert response.status_code == 403


def test_developer_shows_console(admin_logged_client):
    response = admin_logged_client.get('/developer/console')
    assert b'Developer console' in response.data


def test_developer_execute_sql_requires_log_in(client):
    response = client.post('/developer/console/execute_sql',
                           data={
                               'code': 'select * from products'
                           })
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_developer_execute_sql_requires_admin_log_in(org_logged_client):
    response = org_logged_client.post('/developer/console/execute_sql',
                                      data={
                                          'code': 'select * from products'
                                      })
    assert response.status_code == 403


def test_developer_execute_sql_tries_to_execute(admin_logged_client):
    response = admin_logged_client.post('/developer/console/execute_sql',
                                        data={
                                            'code': 'select * from products'
                                        })
    assert response.status_code == 302
    assert '/developer/console' in response.location
