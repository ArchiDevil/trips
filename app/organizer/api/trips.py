from datetime import datetime, timedelta
import hashlib
from uuid import uuid4
from typing import List, Optional, Final

from flask import Blueprint, url_for, abort, g

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import Trip, AccessGroup, TripAccess, SharingLink

BP = Blueprint('trips', __name__, url_prefix='/trips')


@BP.get('/get')
@api_login_required_group(AccessGroup.User)
def get_trip_uids():
    with get_session() as session:
        user_trips: List[Trip] = []
        shared_trips: List[Trip] = []

        if g.user.access_group == AccessGroup.Administrator:
            user_trips = session.query(Trip)
        else:
            user_trips = session.query(Trip).filter(Trip.created_by == g.user.id)
            shared_trips = session.query(Trip.uid).join(TripAccess).filter(TripAccess.user_id == g.user.id,
                                                                           Trip.archived == False).all()
        user_trips = user_trips.filter(Trip.archived == False).all()

        trips = []
        if user_trips:
            for trip in user_trips:
                trips.append(trip.uid)

        if shared_trips:
            for trip in shared_trips:
                trips.append(trip.uid)

        return {'trips': trips}


@BP.get('/get/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def get_info(trip_uid: str):
    with get_session() as session:
        trip: Optional[Trip] = None
        shared = False

        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        if g.user.access_group != AccessGroup.Administrator:
            if trip.created_by != g.user.id:
                shared = True

        magic: Final = int(hashlib.sha1(
            trip.name.encode()).hexdigest(), 16) % 8 + 1

        return {
            'uid': trip.uid,
            'trip': {
                'name': trip.name,
                'from_date': trip.from_date,
                'till_date': trip.till_date,
                'days_count': (trip.till_date - trip.from_date).days + 1,
                'created_by': trip.created_by,
                'last_update': trip.last_update,
                'archived': trip.archived,
                'groups': [group.persons for group in trip.groups],
                'user': trip.user.login,
                'share_link': url_for('api.trips.share', trip_uid=trip.uid),
                'archive_link': url_for('api.trips.archive', trip_uid=trip.uid),
            },
            'type': 'shared' if shared else 'user',
            'attendees': sum(group.persons for group in trip.groups),
            'cover_src': url_for('static', filename=f'img/trips/{magic}.png'),
            'open_link': url_for('meals.days_view', trip_uid=trip.uid),
            'edit_link': url_for('trips.edit', trip_uid=trip.uid),
            'forget_link': url_for('trips.forget', trip_uid=trip.uid),
            'packing_link': url_for('reports.packing', trip_uid=trip.uid),
            'shopping_link': url_for('reports.shopping', trip_uid=trip.uid),
            'download_link': url_for('trips.download', trip_uid=trip.uid),
        }


@BP.get('/share/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def share(trip_uid: str):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        # it could be shared only by a creator or admin
        if trip.created_by != g.user.id and g.user.access_group != AccessGroup.Administrator:
            abort(403)

        link: SharingLink = session.query(SharingLink).filter(
            SharingLink.trip_id == trip.id,
            SharingLink.user_id == g.user.id).first()

        if link:
            uuid = link.uuid
            link.expiration_date = datetime.utcnow() + timedelta(days=3)
            session.commit()
        else:
            uuid = str(uuid4())
            link = SharingLink(uuid=uuid,
                               trip_id=trip.id,
                               user_id=g.user.id)
            session.add(link)
            session.commit()

    return {
        'uuid': uuid,
        'link': url_for('trips.access', uuid=uuid, _external=True, _scheme='https')
    }


@BP.post('/archive/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def archive(trip_uid: str):
    with get_session() as session:
        trip: Optional[Trip] = None

        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        if trip.created_by != g.user.id:
            abort(403)

        trip.archived = True
        trip.last_update = datetime.utcnow()
        session.commit()

    return {'status': 'ok'}
