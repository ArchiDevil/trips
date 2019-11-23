def test_vk_login_provides_correct_link(client):
    response = client.get('/auth/vk_login')
    assert response.status_code == 302
    assert 'https://oauth.vk.com/authorize?' in response.location
    assert 'test_vk_client_id' in response.location
    assert 'client_id' in response.location
    assert 'redirect_uri' in response.location
