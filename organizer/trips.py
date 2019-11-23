import datetime

from flask import Blueprint, render_template, request, url_for, redirect, abort, g, flash

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, AccessGroup, User, TripAccess

bp = Blueprint('trips', __name__)


@bp.route('/')
@login_required_group(AccessGroup.Guest)
def index():
    with get_session() as session:
        user = session.query(User).filter(User.id == g.user.id).one()

        user_trips = None
        shared_trips = None

        if g.user.access_group == AccessGroup.Administrator:
            user_trips = session.query(Trip).filter(Trip.archived == False).all()
        else:
            user_trips = user.trips
            shared_trips = user.shared_trips
        return render_template('trips/trips.html', user_trips=user_trips,
                               shared_trips=shared_trips,
                               no_trips=bool(not user_trips and not shared_trips))


def validate_input_data():
    name = request.form['name']
    if not name:
        raise RuntimeError('Incorrect name provided')

    attendees = request.form['attendees']
    try:
        if not attendees:
            raise ValueError
        attendees = int(attendees)
        if attendees <= 0:
            raise ValueError
    except ValueError:
        raise RuntimeError('Incorrect attendees count provided')

    daterange = request.form['daterange']
    try:
        from_date, till_date = daterange.split(' - ')
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        till_date = datetime.datetime.strptime(till_date, '%Y-%m-%d')
        if till_date < from_date:
            raise ValueError
    except ValueError:
        raise RuntimeError('Incorrect dates provided')
    return name, attendees, from_date, till_date


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
            name, attendees, from_date, till_date = validate_input_data()
        except RuntimeError as exc:
            flash(exc)
            return render_template(template_file,
                                   caption=caption,
                                   submit_caption=submit_caption,
                                   close_url=end_url,
                                   submit_url=add_url)

        with get_session() as session:
            new_trip = Trip(name=name, from_date=from_date,
                            till_date=till_date, attendees=attendees,
                            created_by=g.user.id)
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

        if request.method == 'POST':
            try:
                name, attendees, from_date, till_date = validate_input_data()
            except RuntimeError as exc:
                flash(exc)
                return render_template(template_file,
                                       caption=caption,
                                       trip=trip_info,
                                       archive_button=True,
                                       submit_caption=submit_caption,
                                       close_url=end_url,
                                       submit_url=edit_url)

            trip = session.query(Trip).filter(Trip.id == trip_id).one()
            trip.name = name
            trip.from_date = from_date
            trip.till_date = till_date
            trip.attendees = attendees
            trip.last_update = datetime.datetime.utcnow()
            session.commit()
            return redirect(end_url)

    return render_template(template_file,
                           trip=trip_info,
                           caption=caption,
                           archive_button=True,
                           submit_caption=submit_caption,
                           close_url=end_url,
                           submit_url=edit_url)


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
