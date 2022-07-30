import os
import tempfile

from flask.testing import FlaskClient
import pytest
from organizer import create_app
from organizer.db import re_init_schema, init_connection, init_fake_data


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    application = create_app({
        'TESTING': True,
        'DATABASE': 'sqlite:///' + db_path,
        'VK_CLIENT_ID': 'test_vk_client_id'
    })

    with application.app_context():
        init_connection()
        re_init_schema()
        init_fake_data()

    yield application

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def org_logged_client(client: FlaskClient):
    client.post('/api/auth/login/',
                json={
                    'login': 'Organizer',
                    'password': 'org',
                    'redirect': '/'
                })
    return client


@pytest.fixture
def admin_logged_client(client: FlaskClient):
    client.post('/api/auth/login/',
                json={
                    'login': 'Administrator',
                    'password': 'qwerty',
                    'redirect': '/'
                })
    return client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
