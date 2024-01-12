from flask.testing import FlaskClient

from organizer.db import get_session
from organizer.schema import TripAccess


def test_meals_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/meals/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_meals_shows_non_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/meals/uid3')
    assert response.status_code == 200


def test_meals_shows_page(org_logged_client: FlaskClient):
    response = org_logged_client.get('/meals/uid1')
    assert response.status_code == 200


def test_meals_show_shared_trip_page(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.get('/meals/uid3')
    assert response.status_code == 200


def test_meals_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/meals/uid100')
    assert response.status_code == 404
