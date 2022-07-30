from organizer.strings import STRING_TABLE

def test_developer_requires_log_in(client):
    response = client.get('/developer/administration')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_developer_requires_admin_user(org_logged_client):
    response = org_logged_client.get('/developer/administration')
    assert response.status_code == 403


def test_developer_shows_page(admin_logged_client):
    response = admin_logged_client.get('/developer/administration')
    assert STRING_TABLE['Developer section title'].encode() in response.data
