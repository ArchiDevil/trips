from datetime import datetime, timedelta
from typing import List

from flask.testing import FlaskClient

from organizer.db import get_session
from organizer.strings import STRING_TABLE
from organizer.schema import PasswordLink


def test_forgot_rejects_logged_user(org_logged_client: FlaskClient):
    response = org_logged_client.post('/api/auth/forgot/', json={
        'login': 'Administrator'
    })
    assert response.status_code == 403


def test_forgot_adds_restoration_link_to_db(client: FlaskClient):
    response = client.post('/api/auth/forgot/', json={
        'login': 'Administrator'
    })
    assert response.status_code == 200
    assert response.json
    assert 'message' in response.json
    assert STRING_TABLE['Forgot ok'] == response.json['message']

    with client.application.app_context():
        with get_session() as session:
            links: List[PasswordLink] = session.query(PasswordLink).all()
            assert len(links) == 1
            assert links[0].user_id == 1
            assert links[0].expiration_date.day == (
                datetime.utcnow() + timedelta(days=3)).day


def test_forgot_rejects_incorrect_username(client: FlaskClient):
    response = client.post('/api/auth/forgot/', json={
        'login': 'Inexisting'
    })
    assert response.status_code == 422
    assert response.json
    assert 'message' in response.json
    assert STRING_TABLE['Forgot invalid login'] == response.json['message']
