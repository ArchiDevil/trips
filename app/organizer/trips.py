from datetime import datetime
from typing import Optional

from flask import Blueprint, redirect, abort, g
from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import SharingLink, Trip, AccessGroup, TripAccess

bp = Blueprint('trips', __name__, url_prefix='/trips')


@bp.get('/forget/<trip_uid>')
@login_required_group(AccessGroup.User)
def forget(trip_uid: str):
    with get_session() as session:
        trip: Optional[Trip] = session.query(Trip).filter(
            Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        trip_access = session.query(TripAccess).filter(
            TripAccess.trip_id == trip.id,
            TripAccess.user_id == g.user.id).first()
        if not trip_access:
            abort(403)

        session.delete(trip_access)
        session.commit()

    return redirect('/trips/')


@bp.get('/access/<uuid>')
@login_required_group(AccessGroup.User)
def access(uuid):
    with get_session() as session:
        current_time = datetime.utcnow()
        # clean up dead links
        session.query(SharingLink).filter(SharingLink.expiration_date < current_time).delete()
        session.commit()

        link: Optional[SharingLink] = session.query(SharingLink).filter(SharingLink.uuid == uuid).first()
        if not link:
            return redirect('/trips/incorrect')

        access: Optional[TripAccess] = session.query(TripAccess).filter(
            TripAccess.trip_id == link.trip_id,
            TripAccess.user_id == g.user.id).first()
        if not access:
            session.add(TripAccess(trip_id=link.trip_id, user_id=g.user.id))
            session.commit()

        trip = session.query(Trip).filter(Trip.id == link.trip_id).one()
        return redirect(f'/meals/{trip.uid}')
