import datetime

from flask import Blueprint, render_template, request, url_for, redirect, abort, g

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, AccessGroup, User, TripAccess

bp = Blueprint('trips', __name__)


@bp.route('/')
@login_required_group(AccessGroup.Guest)
def index():
    with get_session() as session:
        if g.user.access_group == AccessGroup.Administrator:
            eligible_trips = session.query(Trip).filter(Trip.archived == False).all()
        else:
            eligible_trips = [y for _, y in session.query(TripAccess,
                                                          Trip).filter(TripAccess.user_id == g.user.id,
                                                                       Trip.id == TripAccess.trip_id,
                                                                       Trip.archived == False).all()]
        return render_template('trips/trips.html', trip_days=eligible_trips, no_trips=bool(not eligible_trips))


@bp.route('/trips/add', methods=['GET', 'POST'])
@login_required_group(AccessGroup.TripManager)
def add():
    if request.method == 'POST':
        # TODO: check if data is correct here
        name = request.form['name']
        daterange = request.form['daterange']
        attendees = request.form['attendees']

        try:
            from_date, till_date = daterange.split(' - ')
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            till_date = datetime.datetime.strptime(till_date, '%Y-%m-%d')
        except ValueError:
            # TODO: do something in case if data is incorrect
            pass

        with get_session() as session:
            new_trip = Trip(name=name, from_date=from_date,
                            till_date=till_date, attendees=attendees)
            session.add(new_trip)
            session.commit()

            user = session.query(User).filter(User.id == g.user.id).one()
            user.trips.append(new_trip)
            session.commit()

        return redirect(url_for('trips.index'))
    return render_template('trips/add.html')


@bp.route('/trips/edit/<int:trip_id>', methods=['GET', 'POST'])
@login_required_group(AccessGroup.TripManager)
def edit(trip_id):
    with get_session() as session:
        if request.method == 'POST':
            # TODO: check if data is correct here
            name = request.form['name']
            daterange = request.form['daterange']
            attendees = request.form['attendees']

            try:
                from_date, till_date = daterange.split(' - ')
                from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
                till_date = datetime.datetime.strptime(till_date, '%Y-%m-%d')
            except ValueError:
                # TODO: do something in case if data is incorrect
                pass

            trip = session.query(Trip).filter(Trip.id == trip_id).one()
            trip.name = name
            trip.from_date = from_date
            trip.till_date = till_date
            trip.attendees = attendees
            trip.last_update = datetime.datetime.utcnow()
            session.commit()
            return redirect(url_for('meals.days_view', trip_id=trip_id))

        trip_info = session.query(Trip).filter(Trip.id == trip_id).one()
    return render_template('trips/edit.html', trip=trip_info, action='edit')


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
