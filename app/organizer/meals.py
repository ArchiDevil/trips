from flask import Blueprint, render_template, abort

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, AccessGroup

bp = Blueprint('meals', __name__, url_prefix='/meals')

@bp.get('/<trip_uid>')
@login_required_group(AccessGroup.User)
def days_view(trip_uid: str):
    with get_session() as session:
        trip: Trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        trip_info = {
            'uid': trip.uid
        }

    return render_template('meals/meals.html', trip=trip_info)
