from flask import Blueprint, abort, request
from werkzeug.security import generate_password_hash

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import AccessGroup, User

BP = Blueprint("users", __name__, url_prefix="/users")


@BP.route("/", methods=["GET", "POST"])
@api_login_required_group(AccessGroup.Administrator)
def index():
    if request.method == "GET":
        with get_session() as session:
            users = session.query(User).all()

            return [
                {
                    "id": user.id,
                    "login": user.login,
                    "displayed_name": user.displayed_name,
                    "last_logged_in": user.last_logged_in,
                    "user_type": user.user_type.name,
                    "access_group": user.access_group.name,
                }
                for user in users
            ], 200
    else:
        if not request.json:
            return abort(400)

        json = request.json
        login = json.get("login")
        password = json.get("password")
        access_group: str = json.get("access_group")

        if not login:
            return abort(400)

        if not password:
            return abort(400)

        if not access_group:
            return abort(400)

        # check if access_group value is a valid AccessGroup enum value
        try:
            AccessGroup[access_group]
        except KeyError:
            return abort(400)

        with get_session() as session:
            # this should actually be done in database schema
            if session.query(User).where(User.login == login).first():
                return abort(400)  # hide the fact that user already exists

            pass_hash = generate_password_hash(password)

            user = User(
                login=login,
                password=pass_hash,
                access_group=AccessGroup[access_group],
            )  # type: ignore
            session.add(user)
            session.commit()

            created_user = session.query(User).where(User.login == login).one()
            return {
                "id": created_user.id,
                "login": created_user.login,
                "user_type": created_user.user_type.name,
                "access_group": created_user.access_group.name,
            }, 201


@BP.put("/<int:user_id>")
@api_login_required_group(AccessGroup.Administrator)
def manage_user(user_id: int):
    if not request.json:
        return abort(400)

    if not request.json.get("access_group"):
        return abort(400)

    access_group = request.json["access_group"]
    try:
        AccessGroup[access_group]
    except KeyError:
        return abort(400)

    with get_session() as session:
        user = session.query(User).where(User.id == user_id).first()

        if not user:
            return abort(404)

        user.access_group = AccessGroup[access_group]
        session.commit()

        return {
            "id": user.id,
            "login": user.login,
            "user_type": user.user_type.name,
            "access_group": user.access_group.name,
        }


@BP.route("/access_groups", methods=["GET"])
@api_login_required_group(AccessGroup.Administrator)
def get_access_groups():
    return [{"id": i, "name": group.name} for i, group in enumerate(AccessGroup)]
