from organizer.db import get_session
from organizer.schema import TripAccess


def test_meals_rejects_not_logged_in(client):
    response = client.get('/meals/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_meals_shows_page(user_logged_client):
    response = user_logged_client.get('/meals/1')
    assert response.status_code == 200
    assert b'Mango' in response.data
    assert b'Taganay' in response.data
    assert b'Day 1' in response.data
    assert b'Day 2' in response.data
    assert b'Day 3' in response.data
    assert b'Day 4' in response.data
    assert b'Day 5' in response.data
    assert b'Total' in response.data
    assert b'Breakfast' in response.data
    assert b'Lunch' in response.data
    assert b'Dinner' in response.data
    assert b'Snacks' in response.data


def test_meals_does_not_show_edit_button_for_guest(user_logged_client):
    response = user_logged_client.get('/meals/1')
    assert b'Edit the trip' not in response.data
    assert b'Packing report' in response.data
    assert b'Shopping report' in response.data


def test_meals_shows_edit_button_for_org(org_logged_client):
    response = org_logged_client.get('/meals/1')
    assert b'Edit the trip' in response.data
    assert b'Packing report' in response.data
    assert b'Shopping report' in response.data


def test_meals_returns_404_for_non_existing_trip(user_logged_client):
    response = user_logged_client.get('/meals/100')
    assert response.status_code == 404


def test_meals_adds_trip_to_user(user_logged_client):
    response = user_logged_client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data
    response = user_logged_client.get('/meals/1')
    response = user_logged_client.get('/')
    assert b'Taganay' in response.data


def test_meals_sharing_does_not_duplicate_existing_access(user_logged_client, app):
    response = user_logged_client.get('/meals/1')
    response = user_logged_client.get('/meals/1')

    with app.test_client() as c:
        rv = c.get('/')
        with get_session() as session:
            result = session.query(TripAccess).filter(TripAccess.trip_id == 1, TripAccess.user_id == 3).all()
            assert len(result) == 1


def test_meals_day_rejects_not_logged_in(client):
    response = client.get('/meals/1/day_table/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_meals_day_returns_404_for_non_existing_trip(user_logged_client):
    response = user_logged_client.get('/meals/100/day_table/1')
    assert response.status_code == 404


def test_meals_day_returns_404_for_non_existing_day(user_logged_client):
    response = user_logged_client.get('/meals/1/day_table/100')
    assert response.status_code == 404


def test_meals_day_returns_day_table(user_logged_client):
    response = user_logged_client.get('/meals/1/day_table/2')
    assert response.status_code == 200
    assert b'Day 2' in response.data
    assert b'Mango' in response.data
    assert b'Breakfast' in response.data
    assert b'Lunch' in response.data
    assert b'Dinner' in response.data
    assert b'Snacks' in response.data
    assert b'Results' in response.data
    assert b'Total' in response.data
