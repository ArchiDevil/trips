from datetime import datetime, timedelta
from uuid import uuid4
import pytest
from flask.testing import FlaskClient
from werkzeug.security import check_password_hash

from organizer.db import get_session
from organizer.schema import PasswordLink, User


def test_can_reset_password(client: FlaskClient):
    uuid = uuid4()
    with client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(uuid=str(uuid), user_id=1))
            session.commit()

    response = client.post('/api/auth/reset/',
                           json={
                               'token': f'{uuid}',
                               'password': 'qwertyempty'
                           })
    assert response.status_code == 200

    with client.application.app_context():
        with get_session() as session:
            password = session.query(User).filter(User.id == 1).one().password
            assert check_password_hash(password, 'qwertyempty')


@pytest.mark.parametrize('json', [
    {'token': 'invalid', 'password': 'qwertyempty'},
    {'token': f'{uuid4()}', 'password': 'short'},
    {'token': '', 'password': 'qwertyempty'},
    {'token': ''},
    {'password': ''}
])
def test_reset_rejects_empty_fields(client: FlaskClient, json: dict):
    uuid = uuid4()
    with client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(uuid=str(uuid), user_id=1))
            session.commit()

    response = client.post('/api/auth/reset/', json=json)
    assert response.status_code == 400

    with client.application.app_context():
        with get_session() as session:
            user_pass = session.query(User).filter(User.id == 1).one().password
            assert check_password_hash(user_pass, 'qwerty')


def test_reset_removes_link(client: FlaskClient):
    uuid = uuid4()
    with client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(uuid=str(uuid), user_id=1))
            session.commit()

    response = client.post('/api/auth/reset/',
                           json={
                               'token': f'{uuid}',
                               'password': 'qwertyempty'
                           })
    assert response.status_code == 200

    with client.application.app_context():
        with get_session() as session:
            password = session.query(User).filter(User.id == 1).one().password
            assert check_password_hash(password, 'qwertyempty')
            link = session.query(PasswordLink).filter(PasswordLink.uuid == str(uuid)).first()
            assert not link


def test_reset_removes_other_dead_links(client: FlaskClient):
    uuid = uuid4()
    with client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(uuid=str(uuid4()), user_id=1, expiration_date=(datetime.utcnow() - timedelta(days=7))))
            session.add(PasswordLink(uuid=str(uuid4()), user_id=2, expiration_date=(datetime.utcnow() - timedelta(days=14))))
            session.add(PasswordLink(uuid=str(uuid4()), user_id=1, expiration_date=(datetime.utcnow() - timedelta(days=21))))
            session.commit()

    response = client.post('/api/auth/reset/',
                           json={
                               'token': f'{uuid}',
                               'password': 'qwertyempty'
                           })
    assert response.status_code == 400

    with client.application.app_context():
        with get_session() as session:
            link = session.query(PasswordLink).all()
            assert not link


def test_reset_rejects_expired_link(client: FlaskClient):
    uuid = uuid4()
    with client.application.app_context():
        with get_session() as session:
            session.add(PasswordLink(uuid=str(uuid), user_id=1, expiration_date=(datetime.utcnow() - timedelta(days=10))))
            session.commit()

    response = client.post('/api/auth/reset/',
                           json={
                               'token': f'{uuid}',
                               'password': 'qwertyempty'
                           })
    assert response.status_code == 400

    with client.application.app_context():
        with get_session() as session:
            password = session.query(User).filter(User.id == 1).one().password
            assert not check_password_hash(password, 'qwertyempty')
            link = session.query(PasswordLink).filter(PasswordLink.uuid == str(uuid)).first()
            assert not link
