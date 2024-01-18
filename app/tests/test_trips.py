from datetime import datetime, timedelta

from flask.testing import FlaskClient

from organizer.schema import SharingLink, Trip, TripAccess
from organizer.db import get_session
from organizer.strings import STRING_TABLE


def test_trips_archive_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/archive/uid100')
    assert response.status_code == 404


def test_trips_forget_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/forget/uid1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_forget_returns_404_for_non_existing_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/forget/uid100')
    assert response.status_code == 404


def test_trips_forget_forgets_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(TripAccess(trip_id=3, user_id=2))
            session.commit()

    response = org_logged_client.get('/trips/forget/uid3')
    assert response.status_code == 302
    assert '/' in response.location

    response = org_logged_client.get('/api/trips/')
    assert response.json
    assert 1 == len(response.json)


def test_trips_forgetting_unknown_rejects(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/forget/uid3')
    assert response.status_code == 403


def test_trips_access_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/trips/access/uid1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_access_rejects_non_existing_uuid(org_logged_client: FlaskClient):
    response = org_logged_client.get('/trips/access/uid42')
    assert response.status_code == 302
    assert '/trips/incorrect' in response.location


def test_trips_access_redirects_to_trip(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(SharingLink(uuid='42', user_id=1, trip_id=3,
                                    expiration_date=datetime.utcnow() + timedelta(days=1)))
            session.commit()

    link = '/trips/access/42'
    response = org_logged_client.get(link)
    assert response.status_code == 302
    assert '/meals/uid3' in response.location


def test_trips_access_gives_access(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(SharingLink(uuid='42', user_id=1, trip_id=3,
                                    expiration_date=datetime.utcnow() + timedelta(days=1)))
            session.commit()

    org_logged_client.get('/trips/access/42')

    with org_logged_client.application.app_context():
        with get_session() as session:
            access = session.query(TripAccess).filter(TripAccess.trip_id == 3).first()
            assert access.user_id == 2


def test_trips_access_does_not_duplicate_access(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(SharingLink(uuid='42', user_id=1, trip_id=3,
                                    expiration_date=datetime.utcnow() + timedelta(days=1)))
            session.commit()

    org_logged_client.get('/trips/access/42')
    org_logged_client.get('/trips/access/42')

    with org_logged_client.application.app_context():
        with get_session() as session:
            count = session.query(TripAccess).filter(TripAccess.trip_id == 3).count()
            assert count == 1


def test_trips_access_expired_links_redirect(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(SharingLink(uuid='42', user_id=1, trip_id=3,
                                    expiration_date=datetime.utcnow() - timedelta(days=1)))
            session.commit()

    response = org_logged_client.get('/trips/access/uid42')
    assert response.status_code == 302
    assert '/trips/incorrect' in response.location

    with org_logged_client.application.app_context():
        with get_session() as session:
            count = session.query(TripAccess).filter(TripAccess.trip_id == 3,
                                                     TripAccess.user_id == 2).count()
            assert count == 0


def test_trips_access_dead_links_removed(org_logged_client: FlaskClient):
    with org_logged_client.application.app_context():
        with get_session() as session:
            session.add(SharingLink(uuid='42', user_id=1, trip_id=3,
                                    expiration_date=datetime.utcnow() - timedelta(days=1)))
            session.add(SharingLink(uuid='54', user_id=2, trip_id=1,
                                    expiration_date=datetime.utcnow() - timedelta(days=1)))
            session.add(SharingLink(uuid='66', user_id=2, trip_id=2,
                                    expiration_date=datetime.utcnow() + timedelta(days=1)))
            session.commit()

    org_logged_client.get('/trips/access/uid42')

    with org_logged_client.application.app_context():
        with get_session() as session:
            count = session.query(SharingLink).count()
            assert count == 1

            link = session.query(SharingLink).first()
            assert link.uuid == '66'
