import datetime
import functools
from typing import List

from flask import Blueprint, render_template, request, url_for, redirect, abort, g, flash

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, AccessGroup, User, TripAccess, Group

bp = Blueprint('trips', __name__)


@bp.route('/')
@login_required_group(AccessGroup.Guest)
def index():
    with get_session() as session:
        user_trips = None
        shared_trips = None

        if g.user.access_group == AccessGroup.Administrator:
            user_trips: List[Trip] = session.query(Trip).all()
        else:
            user = session.query(User).filter(User.id == g.user.id).one()
            user_trips: List[Trip] = user.trips
            shared_trips: List[Trip] = user.shared_trips

        trips = []
        if user_trips:
            for trip in user_trips:
                groups: List[Group] = trip.groups
                trips.append({
                    'trip_record': trip,
                    'type': 'user',
                    'attendees': functools.reduce(lambda x, y: x+y, [group.persons for group in groups])
                })

        if shared_trips:
            for trip in shared_trips:
                groups: List[Group] = trip.groups
                trips.append({
                    'trip_record': trip,
                    'type': 'shared',
                    'attendees': functools.reduce(lambda x, y: x+y, [group.persons for group in groups])
                })

        return render_template('trips/trips.html',
                               trips=trips)


def validate_input_data():
    name = request.form['name']
    if not name:
        raise RuntimeError('Incorrect name provided')

    groups = []
    try:
        i = 1
        while True:
            group_name = 'group{}'.format(i)
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
        raise RuntimeError('Incorrect groups provided')

    daterange = request.form['daterange']
    try:
        from_date, till_date = daterange.split(' - ')
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        till_date = datetime.datetime.strptime(till_date, '%Y-%m-%d')
        if till_date < from_date:
            raise ValueError
    except ValueError:
        raise RuntimeError('Incorrect dates provided')
    return name, groups, from_date, till_date


@bp.route('/trips/add', methods=['GET', 'POST'])
@login_required_group(AccessGroup.TripManager)
def add():
    template_file = 'trips/edit.html'
    caption = 'Add a new trip'
    submit_caption = 'Add'
    add_url = url_for('trips.add')
    end_url = url_for('trips.index')

    if request.method == 'POST':
        try:
            name, groups, from_date, till_date = validate_input_data()
        except RuntimeError as exc:
            flash(exc)
            return render_template(template_file,
                                   caption=caption,
                                   submit_caption=submit_caption,
                                   close_url=end_url,
                                   submit_url=add_url)

        with get_session() as session:
            new_trip = Trip(name=name,
                            from_date=from_date,
                            till_date=till_date,
                            created_by=g.user.id)
            for i, persons in enumerate(groups):
                new_trip.groups.append(Group(group_number=i, persons=persons))
            session.add(new_trip)
            session.commit()
        return redirect(end_url)

    return render_template(template_file,
                           caption=caption,
                           submit_caption=submit_caption,
                           close_url=end_url,
                           submit_url=add_url)


@bp.route('/trips/edit/<int:trip_id>', methods=['GET', 'POST'])
@login_required_group(AccessGroup.TripManager)
def edit(trip_id):
    template_file = 'trips/edit.html'
    caption = 'Edit a trip'
    submit_caption = 'Edit'
    edit_url = url_for('trips.edit', trip_id=trip_id)
    end_url = url_for('meals.days_view', trip_id=trip_id)

    with get_session() as session:
        trip_info = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip_info:
            abort(404)

        trip_groups = [group.persons for group in trip_info.groups]

        if request.method == 'POST':
            try:
                name, groups, from_date, till_date = validate_input_data()
            except RuntimeError as exc:
                flash(exc)
                return render_template(template_file,
                                       caption=caption,
                                       trip=trip_info,
                                       archive_button=True,
                                       submit_caption=submit_caption,
                                       close_url=end_url,
                                       submit_url=edit_url,
                                       groups=trip_groups)

            session.query(Group).filter(Group.trip_id == trip_id).delete()
            session.commit()

            trip = session.query(Trip).filter(Trip.id == trip_id).one()
            trip.name = name
            trip.from_date = from_date
            trip.till_date = till_date
            for i, group in enumerate(groups):
                trip.groups.append(Group(trip_id=trip_id, group_number=i, persons=group))

            trip.last_update = datetime.datetime.utcnow()
            session.commit()
            return redirect(end_url)

    return render_template(template_file,
                           trip=trip_info,
                           caption=caption,
                           archive_button=True,
                           submit_caption=submit_caption,
                           close_url=end_url,
                           submit_url=edit_url,
                           groups=trip_groups)


@bp.route('/trips/archive/<int:trip_id>')
@login_required_group(AccessGroup.TripManager)
def archive(trip_id):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        trip.archived = True
        trip.last_update = datetime.datetime.utcnow()
        session.commit()

    return redirect(url_for('trips.index'))


@bp.route('/trips/forget/<int:trip_id>')
@login_required_group(AccessGroup.Guest)
def forget(trip_id):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        trip_access = session.query(TripAccess).filter(TripAccess.trip_id == trip_id,
                                                       TripAccess.user_id == g.user.id).first()
        if trip_access:
            session.query(TripAccess).filter(TripAccess.trip_id == trip_id,
                                             TripAccess.user_id == g.user.id).delete()
            session.commit()

        return redirect(url_for('trips.index'))
