import csv
from datetime import datetime, timedelta, date, timezone
import io
import secrets
from typing import Any
from uuid import uuid4

from flask import Blueprint, request, send_file, url_for, abort, g
from sentry_sdk import capture_exception
from sqlalchemy import select
from sqlalchemy.orm import Session

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import (
    Group,
    MealRecord,
    Product,
    Trip,
    AccessGroup,
    TripAccess,
    SharingLink,
)
from organizer.strings import STRING_TABLE
from organizer.utils.auth import user_has_trip_access

BP = Blueprint('trips', __name__, url_prefix='/trips')


def gen_trip_uid(session: Session):
    while True:
        new_uid = secrets.token_urlsafe(8)
        existing = session.query(Trip).where(Trip.uid == new_uid).first()
        if not existing:
            return new_uid


def get_trip(trip_uid: str):
    with get_session() as session:
        trip = session.query(Trip).where(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        shared = False
        if g.user.access_group != AccessGroup.Administrator:
            if trip.created_by != g.user.id:
                shared = True

        return {
            'uid': trip.uid,
            'trip': {
                'name': trip.name,
                'from_date': trip.from_date.isoformat(),
                'till_date': trip.till_date.isoformat(),
                'days_count': (trip.till_date - trip.from_date).days + 1,
                'created_by': trip.created_by,
                'last_update': trip.last_update,
                'archived': trip.archived,
                'groups': [group.persons for group in trip.groups],
                'user': trip.user.login,
                'edit_link': url_for('api.trips.edit', trip_uid=trip.uid),
                'copy_link': url_for('api.trips.copy', trip_uid=trip.uid),
                'share_link': url_for('api.trips.share', trip_uid=trip.uid),
                'archive_link': url_for('api.trips.archive', trip_uid=trip.uid),
                'packing_link': f'/reports/packing/{trip.uid}',
                'shopping_link': f'/reports/shopping/{trip.uid}',
                'cycle_link': url_for('api.meals.cycle', trip_uid=trip.uid),
                'download_link': url_for('api.trips.download', trip_uid=trip.uid),
            },
            'type': 'shared' if shared else 'user',
            'attendees': sum(group.persons for group in trip.groups),
            'open_link': f'/meals/{trip.uid}',
            'forget_link': url_for('trips.forget', trip_uid=trip.uid),
        }


@BP.get('/')
@api_login_required_group(AccessGroup.User)
def get_trips():
    with get_session() as session:
        user_trips_req = None
        shared_trips_req = None
        if g.user.access_group == AccessGroup.Administrator:
            user_trips_req = select(Trip)
        else:
            user_trips_req = select(Trip).where(Trip.created_by == g.user.id)
            shared_trips_req = (
                select(Trip.uid)
                .join(TripAccess)
                .where(TripAccess.user_id == g.user.id, Trip.archived == False)
            )
        user_trips_req = user_trips_req.where(Trip.archived == False)

        user_trips = session.execute(user_trips_req).scalars()
        shared_trips = (
            session.execute(shared_trips_req).scalars()
            if shared_trips_req is not None
            else []
        )

        trips = []
        for trip in user_trips:
            trips.append(trip.uid)

        for trip_uids in shared_trips:
            trips.append(trip_uids)

        output = []
        for trip_uid in trips:
            output.append(get_trip(trip_uid))

        return output


@BP.get('/get/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def get_info(trip_uid: str):
    return get_trip(trip_uid)


@BP.get('/share/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def share(trip_uid: str):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        # it could be shared only by a creator or admin
        if (
            trip.created_by != g.user.id
            and g.user.access_group != AccessGroup.Administrator
        ):
            abort(403)

        link = (
            session.query(SharingLink)
            .filter(SharingLink.trip_id == trip.id, SharingLink.user_id == g.user.id)
            .first()
        )

        if link:
            uuid = link.uuid
            link.expiration_date = datetime.now(timezone.utc) + timedelta(days=3)
            session.commit()
        else:
            uuid = str(uuid4())
            link = SharingLink(uuid=uuid, trip_id=trip.id, user_id=g.user.id)
            session.add(link)
            session.commit()

    return {
        'uuid': uuid,
        'link': url_for('trips.access', uuid=uuid, _external=True, _scheme='https'),
    }


@BP.post('/archive/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def archive(trip_uid: str):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        if trip.created_by != g.user.id:
            abort(403)

        trip.archived = True
        trip.last_update = datetime.now(timezone.utc)
        session.commit()

    return {'status': 'ok'}


def validate_edit_input_data(data: dict[str, Any]):
    name: str = data['name']
    if not name or len(name) > 50:
        raise RuntimeError(STRING_TABLE['Trips edit error incorrect name'])

    groups: list[int] = []
    try:
        for group in data['groups']:
            value = int(group)
            if value < 1:
                raise ValueError
            groups.append(group)
        if not groups:
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Trips edit error incorrect groups'])

    try:
        from_date = date.fromisoformat(data['from_date'])
        till_date = date.fromisoformat(data['till_date'])
        if till_date < from_date:
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Trips edit error incorrect dates'])
    return name, groups, from_date, till_date


@BP.post('/add')
@api_login_required_group(AccessGroup.User)
def add():
    try:
        if not request.json:
            raise RuntimeError('No JSON provided')
        name, groups, from_date, till_date = validate_edit_input_data(request.json)
    except RuntimeError as exc:
        capture_exception(exc)
        return abort(400)

    with get_session() as session:
        new_uid = gen_trip_uid(session)
        new_trip = Trip(
            uid=new_uid,
            name=name,
            from_date=from_date,
            till_date=till_date,
            created_by=g.user.id,
        )

        for i, persons in enumerate(groups):
            new_trip.groups.append(Group(group_number=i, persons=persons))

        session.add(new_trip)
        session.commit()

    return get_trip(new_uid)


@BP.post('/edit/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def edit(trip_uid: str):
    try:
        if not request.json:
            raise RuntimeError('No JSON provided')
        name, groups, from_date, till_date = validate_edit_input_data(request.json)
    except RuntimeError as exc:
        capture_exception(exc)
        return abort(400)

    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        if not user_has_trip_access(
            trip, g.user.id, g.user.access_group == AccessGroup.Administrator, session
        ):
            abort(403)

        trip.name = name
        trip.from_date = from_date
        trip.till_date = till_date

        session.query(Group).filter(Group.trip_id == trip.id).delete()
        for i, persons in enumerate(groups):
            trip.groups.append(Group(group_number=i, persons=persons))

        trip.last_update = datetime.now(timezone.utc)
        session.commit()

    return get_trip(trip_uid)


@BP.post('/copy/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def copy(trip_uid: str):
    if not request.json or 'name' not in request.json:
        abort(400)

    new_name = request.json['name']
    if not new_name:
        abort(400)

    with get_session() as session:
        existing_trip = session.query(Trip).where(Trip.uid == trip_uid).first()
        if not existing_trip:
            abort(404)

        if not user_has_trip_access(
            existing_trip,
            g.user.id,
            g.user.access_group == AccessGroup.Administrator,
            session,
        ):
            abort(403)

        new_uid = gen_trip_uid(session)
        new_trip = Trip(
            uid=new_uid,
            name=new_name,
            from_date=existing_trip.from_date,
            till_date=existing_trip.till_date,
            created_by=g.user.id,
        )

        for i, group in enumerate(existing_trip.groups):
            new_trip.groups.append(Group(group_number=i, persons=group.persons))

        session.add(new_trip)
        session.commit()

        new_id = new_trip.id

        meal_records = (
            session.query(MealRecord)
            .where(MealRecord.trip_id == existing_trip.id)
            .all()
        )
        for meal in meal_records:
            session.add(
                MealRecord(
                    trip_id=new_id,
                    product_id=meal.product_id,
                    day_number=meal.day_number,
                    meal_number=meal.meal_number,
                    mass=meal.mass,
                )
            )
        session.commit()

    return get_trip(new_uid)


def send_csv_file(rows: list[list[Any]]):
    file = io.StringIO()
    writer = csv.writer(file, dialect='excel')
    writer.writerows(rows)
    file.seek(0, 0)

    file_to_send = io.BytesIO()
    data = file.read()
    file_to_send.write(bytes([0xEF, 0xBB, 0xBF]))  # write BOM for Excel
    file_to_send.write(data.encode(encoding='utf-8'))
    file_to_send.seek(0, 0)

    return send_file(
        file_to_send,
        mimetype='text/plain',
        as_attachment=True,
        download_name='data.csv',
    )


@BP.get('/download/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def download(trip_uid: str):
    csv_content = [
        [
            STRING_TABLE['CSV name'],
            STRING_TABLE['CSV day'],
            STRING_TABLE['CSV meal'],
            STRING_TABLE['CSV mass'],
            STRING_TABLE['CSV cals'],
        ]
    ]

    meals_table = {
        0: STRING_TABLE['Meals breakfast title'],
        1: STRING_TABLE['Meals lunch title'],
        2: STRING_TABLE['Meals dinner title'],
        3: STRING_TABLE['Meals snacks title'],
    }

    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        days_count = (trip.till_date - trip.from_date).days + 1

        data = session.execute(
            select(
                MealRecord.mass,
                MealRecord.day_number,
                MealRecord.meal_number,
                Product.name,
                Product.calories,
            )
            .join(Product)
            .where(MealRecord.trip_id == trip.id)
            .where(MealRecord.day_number <= days_count)
            .order_by(MealRecord.day_number, MealRecord.meal_number)
        ).all()
        for record in data:
            csv_content.append(
                [
                    record.name,
                    record.day_number,
                    meals_table[record.meal_number],
                    record.mass,
                    record.calories,
                ]
            )

    return send_csv_file(csv_content)
