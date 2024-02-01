from flask.testing import FlaskClient
import pytest

from organizer.db import get_session
from organizer.schema import AccessGroup, User, UserType


def test_group_rejects_non_admin_client(org_logged_client: FlaskClient):
    response = org_logged_client.get("/api/users/access_groups")
    assert response.status_code == 403


def test_can_access_groups(admin_logged_client: FlaskClient):
    response = admin_logged_client.get("/api/users/access_groups")
    assert response.status_code == 200
    assert response.json
    assert len(response.json) == 2

    assert response.json[0]["id"] == 0
    assert response.json[0]["name"] == AccessGroup.User.name

    assert response.json[1]["id"] == 1
    assert response.json[1]["name"] == AccessGroup.Administrator.name


def test_user_api_returns_unauthorized_for_non_logged_in_user(client: FlaskClient):
    response = client.get("/api/auth/user")
    assert response.status_code == 401


def test_can_get_user_info(org_logged_client: FlaskClient):
    response = org_logged_client.get("/api/auth/user")
    assert response.status_code == 200
    assert response.json
    assert response.json["id"]
    assert "Organizer" == response.json["login"]
    assert AccessGroup.User.name == response.json["access_group"]
    assert UserType.Native.name == response.json["user_type"]


def test_rejects_non_logged_client(client: FlaskClient):
    response = client.get("/api/users/")
    assert response.status_code == 401


def test_rejects_non_admin_client(org_logged_client: FlaskClient):
    response = org_logged_client.get("/api/users/")
    assert response.status_code == 403


def test_can_get_users(admin_logged_client: FlaskClient):
    response = admin_logged_client.get("/api/users/")
    assert response.status_code == 200
    assert response.json
    assert len(response.json) == 2

    assert response.json[0]["id"] == 1
    assert response.json[0]["login"] == "Administrator"
    assert response.json[0]["user_type"] == UserType.Native.name
    assert response.json[0]["access_group"] == AccessGroup.Administrator.name

    assert response.json[1]["id"] == 2
    assert response.json[1]["login"] == "Organizer"
    assert response.json[1]["user_type"] == UserType.Native.name
    assert response.json[1]["access_group"] == AccessGroup.User.name


def test_add_rejects_non_logged_user(client: FlaskClient):
    response = client.post(
        "/api/users/",
        json={
            "login": "test",
            "password": "test",
            "access_group": AccessGroup.User.name,
        },
    )
    assert response.status_code == 401


def test_add_rejects_non_admin_client(org_logged_client: FlaskClient):
    response = org_logged_client.post(
        "/api/users/",
        json={
            "login": "test",
            "password": "test",
            "access_group": AccessGroup.User.name,
        },
    )
    assert response.status_code == 403


def test_can_add_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.post(
        "/api/users/",
        json={
            "login": "test",
            "password": "test",
            "access_group": AccessGroup.User.name,
        },
    )
    assert response.status_code == 201
    assert response.json
    assert response.json["id"] == 3
    assert response.json["login"] == "test"
    assert response.json["user_type"] == UserType.Native.name
    assert response.json["access_group"] == AccessGroup.User.name

    with admin_logged_client.application.app_context():
        with get_session() as session:
            user = session.query(User).where(User.login == "test").first()
            assert user
            # check that password is not stored as a provided string
            assert user.password != "test"


@pytest.mark.parametrize(
    "json_data",
    [
        {},  # empty json
        {
            "login": "Administrator",
            "password": "test",
            "access_group": AccessGroup.Administrator.name,
        },
        {
            "login": "",
            "password": "test",
            "access_group": AccessGroup.Administrator.name,
        },
        {
            "login": "New",
            "password": "",
            "access_group": AccessGroup.Administrator.name,
        },
        {
            "login": "New",
            "password": "pass",
            "access_group": "Incorrect",
        },
        {
            "login": "New",
            "password": "pass",
            "access_group": "",
        },
        {
            "password": "pass",
            "access_group": AccessGroup.User.name,
        },
        {
            "login": "New",
            "access_group": AccessGroup.Administrator.name,
        },
        {
            "login": "New",
            "password": "test",
        },
    ],
)
def test_add_rejects_incorrect_data(admin_logged_client: FlaskClient, json_data):
    response = admin_logged_client.post(
        "/api/users/",
        json=json_data,
    )
    assert response.status_code == 400

    if json_data.get("login") and not json_data.get("login") == "Administrator":
        with admin_logged_client.application.app_context():
            with get_session() as session:
                assert (
                    not session.query(User)
                    .where(User.login == json_data["login"])
                    .first()
                )


def test_edit_rejects_non_logged_user(client: FlaskClient):
    response = client.put(
        "/api/users/1",
        json={
            "access_group": AccessGroup.User.name,
        },
    )
    assert response.status_code == 401


def test_edit_rejects_non_admin_client(org_logged_client: FlaskClient):
    response = org_logged_client.put(
        "/api/users/1",
        json={
            "access_group": AccessGroup.User.name,
        },
    )
    assert response.status_code == 403


def test_can_edit_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.put(
        "/api/users/1",
        json={
            "access_group": AccessGroup.User.name,
        },
    )
    assert response.status_code == 200
    assert response.json
    assert response.json["id"] == 1
    assert response.json["login"] == "Administrator"
    assert response.json["user_type"] == UserType.Native.name
    assert response.json["access_group"] == AccessGroup.User.name

    with admin_logged_client.application.app_context():
        with get_session() as session:
            user = session.query(User).where(User.id == 1).first()
            assert user
            assert user.access_group == AccessGroup.User


def test_edit_rejects_non_existing_user(admin_logged_client: FlaskClient):
    response = admin_logged_client.put(
        "/api/users/3",
        json={
            "access_group": AccessGroup.User.name,
        },
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "json_data",
    [
        {},
        {
            "access_group": "Incorrect",
        },
    ],
)
def test_edit_rejects_incorrect_data(admin_logged_client: FlaskClient, json_data):
    response = admin_logged_client.put(
        "/api/users/1",
        json=json_data,
    )
    assert response.status_code == 400

    with admin_logged_client.application.app_context():
        with get_session() as session:
            user = session.query(User).where(User.id == 1).first()
            assert user
            assert user.access_group == AccessGroup.Administrator
