from flask import Blueprint, render_template, request, url_for, redirect
import flask

from organizer.db import get_db

bp = Blueprint('trips', __name__)


@bp.route('/')
def index():
    db = get_db()
    days = db.execute(
        'SELECT id, name, from_date, till_date, last_update FROM trips WHERE archived=0'
    ).fetchall()

    return render_template('trips/trips.j2', trip_days=days)


@bp.route('/trips/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        daterange = request.form['daterange']
        attendees = request.form['attendees']

        from_date, till_date = daterange.split(' - ')

        db = get_db()
        db.execute(
            'INSERT INTO trips(name, from_date, till_date, attendees) VALUES (?, ?, ?, ?)',
            (name, from_date, till_date, attendees)
        )
        db.commit()

        return redirect(url_for('trips.index'))

    return render_template('trips/add.j2')


@bp.route('/trips/trip/<int:trip_id>')
def trip(trip_id):
    db = get_db()

    trip_info = db.execute(
        'SELECT id, name, from_date, till_date FROM trips WHERE id=?',
        (trip_id,)
    ).fetchone()

    return render_template('trips/days.j2', trip=trip_info)


@bp.route('/trips/edit/<int:trip_id>', methods=('GET', 'POST'))
def edit(trip_id):
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        daterange = request.form['daterange']
        attendees = request.form['attendees']

        from_date, till_date = daterange.split(' - ')

        db.execute(
            'UPDATE trips SET name=?, from_date=?, till_date=?, attendees=? WHERE id=?',
            (name, from_date, till_date, attendees, trip_id)
        )
        db.commit()

        return redirect(url_for('trips.trip', trip_id=trip_id))

    trip_info = db.execute(
        'SELECT id, name, from_date, till_date, attendees FROM trips WHERE id=?',
        (trip_id,)
    ).fetchone()

    return render_template('trips/edit.j2', trip=trip_info, action='edit')


@bp.route('/trips/archive/<int:trip_id>')
def archive(trip_id):
    db = get_db()
    db.execute(
        'UPDATE trips SET archived=1 WHERE id=?',
        (trip_id,)
    )
    db.commit()

    return redirect(url_for('trips.index'))
