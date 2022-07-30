import datetime

from flask.app import Flask
from flask.testing import FlaskClient

from organizer.schema import TripAccess, TripAccessType, VkUser
from organizer.db import get_session
from organizer.strings import STRING_TABLE

def test_users_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/users/')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_users_rejects_trip_managers(org_logged_client: FlaskClient):
    response = org_logged_client.get('/users/')
    assert response.status_code == 403


def test_users_shows_users(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/users/')
    assert response.status_code == 200
    assert b'Organizer' in response.data
    assert b'Administrator' in response.data


def test_users_add_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/users/add')
    assert response.status_code == 302
    assert '/auth/login' in response.location

    response = client.post('/users/add',
                           data={
                               'login': 'test',
                               'password': '123',
                               'group': 'Guest'
                           })
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_users_add_rejects_trip_managers(org_logged_client: FlaskClient):
    response = org_logged_client.get('/users/add')
    assert response.status_code == 403

    response = org_logged_client.post('/users/add',
                                      data={
                                          'login': 'test',
                                          'password': '123',
                                          'group': 'Guest'
                                      })
    assert response.status_code == 403


def test_users_add_shows_page(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/users/add')
    assert response.status_code == 200


def test_users_add_adds_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'login': 'Test user',
                                            'password': '123',
                                            'group': 'User'
                                        })
    assert response.status_code == 302
    assert '/users/' in response.location

    response = admin_logged_client.get('/users/')
    assert b'Test user' in response.data


def test_users_add_rejects_empty_name(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'login': '',
                                            'password': '123',
                                            'group': 'User'
                                        })
    assert response.status_code == 200
    assert STRING_TABLE['User edit error empty login'].encode() in response.data


def test_users_add_rejects_existing_name(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'login': 'Administrator',
                                            'password': '123',
                                            'group': 'User'
                                        })
    assert response.status_code == 200
    assert STRING_TABLE['User edit error existing login'].encode() in response.data


def test_users_add_rejects_empty_password(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'login': 'Test user',
                                            'password': '',
                                            'group': 'User'
                                        })
    assert response.status_code == 200
    assert STRING_TABLE['User edit error empty password'].encode() in response.data

    response = admin_logged_client.get('/users/')
    assert b'Test user' not in response.data


def test_users_add_rejects_empty_group(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'login': 'Test user',
                                            'password': '123',
                                            'group': ''
                                        })
    assert response.status_code == 200
    assert STRING_TABLE['User edit error empty group'].encode() in response.data

    response = admin_logged_client.get('/users/')
    assert b'Test user' not in response.data


def test_users_add_rejects_wrong_group(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/add',
                                        data={
                                            'login': 'Test user',
                                            'password': '123',
                                            'group': 'WRONG'
                                        })
    assert response.status_code == 200
    assert STRING_TABLE['User edit error wrong group'].encode() in response.data

    response = admin_logged_client.get('/users/')
    assert b'Test user' not in response.data


def test_users_remove_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/users/remove/2')
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_users_remove_rejects_trip_managers(org_logged_client: FlaskClient):
    response = org_logged_client.get('/users/remove/2')
    assert response.status_code == 403


def test_users_remove_removes_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/users/remove/2')
    assert response.status_code == 302
    assert '/users/' in response.location

    response = admin_logged_client.get('/users/')
    assert b'Organizer' not in response.data


def test_users_remove_returns_404_on_wrong_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/users/remove/1000')
    assert response.status_code == 404


def test_users_remove_cannot_remove_current_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/users/remove/1')
    assert response.status_code == 403  # forbidden to remove current user


def test_users_remove_trip_access(admin_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            session.add(TripAccess(user_id=2, trip_id=1, access_type=TripAccessType.Read))
            session.commit()

    response = admin_logged_client.get('/users/remove/2')
    assert response.status_code == 302
    assert '/users/' in response.location

    with app.app_context():
        with get_session() as session:
            assert not session.query(TripAccess).filter(TripAccess.user_id == 2).first()


def test_users_remove_vk_user(admin_logged_client: FlaskClient, app: Flask):
    with app.app_context():
        with get_session() as session:
            session.add(VkUser(id=12,
                               user_id=2,
                               user_token="12345",
                               token_exp_time=datetime.datetime.utcnow()))
            session.commit()

    response = admin_logged_client.get('/users/remove/2')
    assert response.status_code == 302
    assert '/users/' in response.location

    with app.app_context():
        with get_session() as session:
            assert not session.query(VkUser).filter(VkUser.user_id == 2).first()


def test_users_edit_rejects_not_logged_in(client: FlaskClient):
    response = client.get('/users/edit/1')
    assert response.status_code == 302
    assert '/auth/login' in response.location

    response = client.post('/users/edit/1',
                           data={
                               'name': 'test',
                               'password': '123',
                               'group': 'Guest'
                           })
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_users_edit_rejects_trip_managers(org_logged_client: FlaskClient):
    response = org_logged_client.get('/users/edit/1')
    assert response.status_code == 403

    response = org_logged_client.post('/users/edit/1',
                                      data={
                                          'name': 'test',
                                          'password': '123',
                                          'group': 'Guest'
                                      })
    assert response.status_code == 403


def test_users_edit_shows_page(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/users/edit/1')
    assert response.status_code == 200
    assert STRING_TABLE['User edit edit button'].encode() in response.data
    assert b'Administrator' in response.data


def test_users_rejects_for_non_existing_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.get('/users/edit/100')
    assert response.status_code == 404


def test_users_edit_edits_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/edit/1',
                                        data={
                                            'group': 'User'
                                        })
    assert response.status_code == 302
    assert '/users/' in response.location

    response = admin_logged_client.get('/users/')
    assert b'Administrator' not in response.data


def test_users_edit_edits_user_group(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/edit/1',
                                        data={
                                            'login': 'Organizer',
                                            'group': 'Administrator'
                                        })
    assert response.status_code == 302
    assert '/users/' in response.location

    response = admin_logged_client.get('/users/')
    assert b'Organizer' in response.data


def test_users_edit_rejects_empty_group(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/edit/1',
                                        data={
                                            'group': ''
                                        })
    assert response.status_code == 200
    assert STRING_TABLE['User edit error empty group'].encode() in response.data


def test_users_edit_rejects_wrong_group(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/edit/1',
                                        data={
                                            'group': 'WRONG'
                                        })
    assert response.status_code == 200
    assert STRING_TABLE['User edit error wrong group'].encode() in response.data

    response = admin_logged_client.get('/users/')
    assert b'WRONG' not in response.data


def test_users_edit_rejects_non_existing_id_post(admin_logged_client: FlaskClient):
    response = admin_logged_client.post('/users/edit/100',
                                        data={
                                            'group': 'Administrator'
                                        })
    assert response.status_code == 404
