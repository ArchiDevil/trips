import hashlib
from typing import List, Optional, Final

from flask import Blueprint, url_for, abort, g

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import Trip, AccessGroup, TripAccess

BP = Blueprint('trips', __name__, url_prefix='/trips')


@BP.get('/get')
@api_login_required_group(AccessGroup.Guest)
def get_trip_ids():
    with get_session() as session:
        user_trips: List[Trip] = []
        shared_trips: List[Trip] = []

        if g.user.access_group == AccessGroup.Administrator:
            user_trips = session.query(Trip).filter(Trip.archived == False).all()
        else:
            user_trips = session.query(Trip).filter(Trip.created_by == g.user.id,
                                                    Trip.archived == False).all()
            shared_trips = session.query(TripAccess.trip_id).filter(TripAccess.user_id == g.user.id,
                                                                    Trip.id == TripAccess.trip_id,
                                                                    Trip.archived == False).all()

        trips = []
        if user_trips:
            for trip in user_trips:
                trips.append(trip.id)

        if shared_trips:
            for trip in shared_trips:
                trips.append(trip.trip_id)

        return {'trips': trips}


@BP.get('/get/<int:trip_id>')
@api_login_required_group(AccessGroup.Guest)
def get_info(trip_id):
    with get_session() as session:
        trip: Optional[Trip] = None
        shared = False

        trip = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        if g.user.access_group != AccessGroup.Administrator:
            if trip.created_by != g.user.id:
                if not session.query(TripAccess).filter(TripAccess.trip_id == trip_id,
                                                        TripAccess.user_id == g.user.id).first():
                    abort(403)
                shared = True

        magic: Final = int(hashlib.sha1(
            trip.name.encode()).hexdigest(), 16) % 8 + 1

        return {
            'id': trip_id,
            'trip': {
                'name': trip.name,
                'from_date': trip.from_date,
                'till_date': trip.till_date,
                'days_count': (trip.till_date - trip.from_date).days + 1,
                'created_by': trip.created_by,
                'last_update': trip.last_update,
                'archived': trip.archived,
                'groups': [group.persons for group in trip.groups],
                'user': trip.user.login
            },
            'type': 'shared' if shared else 'user',
            'attendees': sum([group.persons for group in trip.groups]),
            'cover_src': url_for('static', filename=f'img/trips/{magic}.png'),
            'open_link': url_for('meals.days_view', trip_id=trip_id),
            'edit_link': url_for('trips.edit', trip_id=trip_id),
            'forget_link': url_for('trips.forget', trip_id=trip_id),
            'packing_link': url_for('reports.packing', trip_id=trip_id),
            'shopping_link': url_for('reports.shopping', trip_id=trip_id),
            'download_link': url_for('trips.download', trip_id=trip_id)
        }
