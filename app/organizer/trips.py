import csv
import io
from datetime import datetime
from typing import Any, List, Optional

from flask import Blueprint, render_template, request, url_for, redirect, \
                  abort, g, flash, send_file
from sentry_sdk import capture_exception

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import SharingLink, Trip, AccessGroup, TripAccess, Group, \
                             Product, MealRecord
from organizer.strings import STRING_TABLE
from organizer.utils.auth import user_has_trip_access

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


def send_csv_file(rows: List[List[Any]]):
    file = io.StringIO()
    writer = csv.writer(file, dialect='excel')
    writer.writerows(rows)
    file.seek(0, 0)

    file_to_send = io.BytesIO()
    data = file.read()
    file_to_send.write(bytes([0xEF, 0xBB, 0xBF])) # write BOM for Excel
    file_to_send.write(data.encode(encoding='utf-8'))
    file_to_send.seek(0, 0)

    return send_file(file_to_send, mimetype='text/plain',
                     as_attachment=True, download_name='data.csv')


@bp.get('/download/<trip_uid>')
@login_required_group(AccessGroup.User)
def download(trip_uid: str):
    csv_content = [[
        STRING_TABLE['CSV name'],
        STRING_TABLE['CSV day'],
        STRING_TABLE['CSV meal'],
        STRING_TABLE['CSV mass'],
        STRING_TABLE['CSV cals']
    ]]

    meals_table = {
        0: STRING_TABLE['Meals breakfast title'],
        1: STRING_TABLE['Meals lunch title'],
        2: STRING_TABLE['Meals dinner title'],
        3: STRING_TABLE['Meals snacks title']
    }

    with get_session() as session:
        trip: Optional[Trip] = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        data = session.query(MealRecord.mass,
                             MealRecord.day_number,
                             MealRecord.meal_number,
                             Product.name,
                             Product.calories).join(Product).order_by(MealRecord.day_number,
                                                                      MealRecord.meal_number).filter(MealRecord.trip_id == trip.id).all()
        for record in data:
            csv_content.append([record.name,
                                record.day_number,
                                meals_table[record.meal_number],
                                record.mass,
                                record.calories])

    return send_csv_file(csv_content)


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
            return redirect(url_for('trips.incorrect'))

        access: Optional[TripAccess] = session.query(TripAccess).filter(
            TripAccess.trip_id == link.trip_id,
            TripAccess.user_id == g.user.id).first()
        if not access:
            session.add(TripAccess(trip_id=link.trip_id, user_id=g.user.id))
            session.commit()

        trip = session.query(Trip).filter(Trip.id == link.trip_id).one()
        return redirect(url_for('meals.days_view', trip_uid=trip.uid))


@bp.get('/incorrect')
@login_required_group(AccessGroup.User)
def incorrect():
    return render_template('trips/incorrect.html')
