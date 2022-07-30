from organizer import create_app
from organizer.schema import AccessGroup


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_init_db_command(runner, monkeypatch):
    class Recorder():
        called = False

    def interceptor():
        Recorder.called = True

    monkeypatch.setattr('organizer.db.re_init_schema', interceptor)
    result = runner.invoke(args=['init-empty-db'])
    assert 'Initialized the database' in result.output
    assert Recorder.called


def test_init_fake_data_command(runner, monkeypatch):
    class Recorder():
        called = False

    def interceptor():
        Recorder.called = True

    monkeypatch.setattr('organizer.db.init_fake_data', interceptor)
    result = runner.invoke(args=['init-fake-data'])
    assert 'Tables filled with fake data' in result.output
    assert Recorder.called


def test_create_admin_command(runner, monkeypatch):
    called = False

    def interceptor(login, password, access_group):
        assert login == 'some_login'
        assert password == 'password'
        assert access_group == AccessGroup.Administrator

        nonlocal called
        called = True

    monkeypatch.setattr('organizer.db.create_user', interceptor)
    result = runner.invoke(args=['create-admin', 'some_login', 'password'])
    assert 'Successfully created admin "some_login"' in result.output
    assert called


def test_create_admin_creates(runner, client):
    runner.invoke(args=['create-admin', 'some_login', 'password'])
    response = client.post('/api/auth/login/',
                           json={
                               'login': 'some_login',
                               'password': 'password'
                            })
    assert response.status_code == 200
    assert 'message' in response.json
