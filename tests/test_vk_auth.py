from urllib.parse import urlencode

def test_vk_login_provides_correct_link(client):
    response = client.get('/auth/vk_login?redirect=/')
    assert response.status_code == 302
    assert 'https://oauth.vk.com/authorize?' in response.location
    assert 'test_vk_client_id' in response.location
    assert 'client_id' in response.location
    assert 'redirect_uri' in response.location
    assert 'state' in response.location


def test_vk_login_requests_data_after_redirection(client, monkeypatch):
    class Recorder():
        token_called = False
        user_info_called = False

    fake_access_token = 'token'
    fake_user_id = 87654
    fake_code = 'fake_code'
    fake_redirect = 'something'

    def token_interceptor(code):
        assert code == fake_code
        Recorder.token_called = True
        return fake_access_token, 1234, fake_user_id

    def user_info_interceptor(access_token):
        assert access_token == fake_access_token
        Recorder.user_info_called = True
        return 'Adams Brown', 'url.url'

    monkeypatch.setattr('organizer.auth.request_vk_access_token', token_interceptor)
    monkeypatch.setattr('organizer.auth.request_vk_user_name_and_photo', user_info_interceptor)

    response = client.get('/auth/vk_redirect?' +
                          urlencode({
                              'code': fake_code,
                              'state': fake_redirect
                          }))

    assert response.status_code == 302
    assert fake_redirect in response.location
    assert Recorder.token_called
    assert Recorder.user_info_called


def test_vk_login_logins_for_existing_user(client, monkeypatch):
    class Recorder():
        token_called = False
        user_info_called = False

    fake_access_token = 'token'
    fake_user_id = 87654
    fake_code = 'fake_code'
    fake_redirect = 'something'

    def token_interceptor(code):
        assert code == fake_code
        Recorder.token_called = True
        return fake_access_token, 1234, fake_user_id

    def user_info_interceptor(access_token):
        assert access_token == fake_access_token
        Recorder.user_info_called = True
        return 'Adams Brown', 'url.url'

    monkeypatch.setattr('organizer.auth.request_vk_access_token', token_interceptor)
    monkeypatch.setattr('organizer.auth.request_vk_user_name_and_photo', user_info_interceptor)

    client.get('/auth/vk_redirect?' +
               urlencode({
                   'code': fake_code,
                   'state': fake_redirect
               }))
    response = client.get('/auth/logout')
    assert response.status_code == 302

    response = client.get('/auth/vk_redirect?' +
                          urlencode({
                              'code': fake_code,
                              'state': fake_redirect
                          }))
    assert response.status_code == 302
    assert fake_redirect in response.location
    assert Recorder.token_called
    assert Recorder.user_info_called
