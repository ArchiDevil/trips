import os
import tempfile

import pytest
from organizer import create_app
from organizer.db import re_init_schema, init_connection, init_fake_data


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    application = create_app({
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///' + db_path,
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
def runner(app):
    return app.test_cli_runner()