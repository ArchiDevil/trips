import csv
import io
from datetime import datetime
from typing import Any, List, Optional
import secrets

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


def validate_input_data():
    name = request.form['name']
    if not name or len(name) > 50:
        raise RuntimeError(STRING_TABLE['Trips edit error incorrect name'])

    groups = []
    try:
        i = 1
        while True:
            group_name = f'group{i}'
            if group_name in request.form:
                value = int(request.form[group_name])
                if value < 1:
                    raise ValueError
                groups.append(request.form[group_name])
                i += 1
            else:
                break
        if not groups:
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Trips edit error incorrect groups'])

    daterange = request.form['daterange']
    try:
        from_date, till_date = daterange.split(' - ')
        from_date = datetime.strptime(from_date, '%d-%m-%Y')
        till_date = datetime.strptime(till_date, '%d-%m-%Y')
        if till_date < from_date:
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Trips edit error incorrect dates'])
    return name, groups, from_date, till_date


@bp.route('/add', methods=['GET', 'POST'])
@login_required_group(AccessGroup.User)
def add():
    template_file = 'trips/edit.html'
    caption = STRING_TABLE['Trips add title']
    submit_caption = STRING_TABLE['Trips add edit button']
    add_url = url_for('.add')
    end_url = '/trips/'

    if request.method == 'POST':
        try:
            name, groups, from_date, till_date = validate_input_data()
        except RuntimeError as exc:
            capture_exception(exc)
            flash(exc)
            return render_template(template_file,
                                   caption=caption,
                                   submit_caption=submit_caption,
                                   close_url=end_url,
                                   submit_url=add_url)

        with get_session() as session:
            while True:
                new_uid = secrets.token_urlsafe(8)
                existing = session.query(Trip).filter(Trip.uid == new_uid).first()
                if not existing:
                    break

            new_trip = Trip(
                uid=new_uid,
                name=name,
                from_date=from_date,
                till_date=till_date,
                created_by=g.user.id)

            for i, persons in enumerate(groups):
                new_trip.groups.append(Group(group_number=i, persons=persons))

            session.add(new_trip)
            session.commit()

            end_url = url_for('meals.days_view', trip_uid=new_trip.uid)
        return redirect(end_url)

    return render_template(template_file,
                           caption=caption,
                           submit_caption=submit_caption,
                           close_url='/trips/',
                           submit_url=add_url)


@bp.route('/edit/<trip_uid>', methods=['GET', 'POST'])
@login_required_group(AccessGroup.User)
def edit(trip_uid: str):
    template_file = 'trips/edit.html'
    caption = STRING_TABLE['Trips edit title']
    submit_caption = STRING_TABLE['Trips edit edit button']
    edit_url = url_for('trips.edit', trip_uid=trip_uid)
    redirect_location = request.referrer if request.referrer else request.headers.get('Referer')
    if not redirect_location:
        redirect_location = '/trips/'

    with get_session() as session:
        trip_info = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip_info:
            abort(404)

        if not user_has_trip_access(trip_info,
                                    g.user.id,
                                    g.user.access_group == AccessGroup.Administrator,
                                    session):
            abort(403)

        trip_groups = [group.persons for group in trip_info.groups]

        if request.method == 'POST':
            try:
                name, groups, from_date, till_date = validate_input_data()
                if not 'redirect' in request.form:
                    # actually this error must never be visible by a user
                    # because this is internal one
                    raise RuntimeError('No redirect field is provided')
            except RuntimeError as exc:
                capture_exception(exc)
                flash(exc)
                return render_template(template_file,
                                       caption=caption,
                                       trip=trip_info,
                                       archive_button=True,
                                       submit_caption=submit_caption,
                                       close_url='/trips/',
                                       submit_url=edit_url,
                                       groups=trip_groups,
                                       redirect='/trips/')

            redirect_location = request.form['redirect']
            session.query(Group).filter(Group.trip_id == trip_info.id).delete()
            session.commit()

            trip = session.query(Trip).filter(Trip.id == trip_info.id).one()
            trip.name = name
            trip.from_date = from_date
            trip.till_date = till_date
            for i, group in enumerate(groups):
                trip.groups.append(Group(trip_id=trip.id, group_number=i, persons=group))

            trip.last_update = datetime.utcnow()
            session.commit()
            return redirect(redirect_location)

    return render_template(template_file,
                           trip=trip_info,
                           caption=caption,
                           archive_button=True,
                           submit_caption=submit_caption,
                           close_url=redirect_location,
                           submit_url=edit_url,
                           groups=trip_groups,
                           redirect=redirect_location)


@bp.get('/archive/<trip_uid>')
@login_required_group(AccessGroup.User)
def archive(trip_uid: str):
    with get_session() as session:
        trip: Optional[Trip] = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        if trip.created_by != g.user.id:
            abort(403)

        trip.archived = True
        trip.last_update = datetime.utcnow()
        session.commit()

    return redirect('/trips/')


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
