from organizer import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('organizer.db.re_init_schema', fake_init_db)
    result = runner.invoke(args=['init-empty-db'])
    assert 'Initialized the database' in result.output
    assert Recorder.called


def test_init_fake_data_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('organizer.db.init_fake_data', fake_init_db)
    result = runner.invoke(args=['init-fake-data'])
    assert 'Tables filled with fake data' in result.output
    assert Recorder.called
