from flask import Blueprint, g

from organizer.auth import api_login_required_group
from organizer.schema import AccessGroup

BP = Blueprint('auth', __name__, url_prefix='/auth')


@BP.get('/user')
@api_login_required_group(AccessGroup.User)
def user():
    return {
        'id': g.user.id,
        'login': g.user.login,
        'displayed_name': g.user.displayed_name,
        'access_group': g.user.access_group.name,
        'user_type': g.user.user_type.name,
    }
