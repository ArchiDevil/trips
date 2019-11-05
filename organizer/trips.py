import datetime
from typing import List

from flask import Blueprint, render_template, request, url_for, redirect, get_template_attribute

from organizer.db import get_db

bp = Blueprint('trips', __name__)


def format_date(first_day, current_day_number):
    y = (first_day + datetime.timedelta(days=current_day_number - 1)).year
    m = (first_day + datetime.timedelta(days=current_day_number - 1)).month
    d = (first_day + datetime.timedelta(days=current_day_number - 1)).day
    return '{:4}-{:02}-{:02}'.format(y, m, d)


def calculate_day_info(day_number : int,
                       date: str,
                       attendees_count : int,
                       meals_info : List[dict]):
    day = {
        'number': day_number,
        'date': '',
        'breakfast': [],
        'breakfast_total': {'mass': 0},
        'lunch': [],
        'lunch_total': {'mass': 0},
        'dinner': [],
        'dinner_total': {'mass': 0},
        'snacks': [],
        'snacks_total': {'mass': 0},
        'total_total': {'mass': 0}
    }

    meals_map = {
        0: 'breakfast',
        1: 'lunch',
        2: 'dinner',
        3: 'snacks'
    }

    for record in meals_info:
        meal_number = record['meal_number']
        day[meals_map[meal_number]].append(
            {
                'id': record['id'],
                'name': record['name'],
                'mass': record['mass'],
                'proteins': record['proteins'] * record['mass'] / 100.0,
                'fats': record['fats'] * record['mass'] / 100.0,
                'carbs': record['carbs'] * record['mass'] / 100.0,
                'cals': record['calories'] * record['mass'] / 100.0
            }
        )

    # calculating totals for each day
    for field in ('mass', 'proteins', 'fats', 'carbs', 'cals'):
        day['breakfast_total'][field] = sum([e[field] for e in day['breakfast']])
        day['lunch_total'][field] = sum([e[field] for e in day['lunch']])
        day['dinner_total'][field] = sum([e[field] for e in day['dinner']])
        day['snacks_total'][field] = sum([e[field] for e in day['snacks']])

        day['total_total'][field] = sum([day['breakfast_total'][field],
                                         day['lunch_total'][field],
                                         day['dinner_total'][field],
                                         day['snacks_total'][field]])

    day['date'] = date
    return day


def calculate_total_days_info(first_date, last_date, attendees_count, meals_info):
    days_amount = (last_date - first_date).days + 1
    days = [
        {
            'number': x,
            'date': '',
            'breakfast': [],
            'breakfast_total': {'mass': 0},
            'lunch': [],
            'lunch_total': {'mass': 0},
            'dinner': [],
            'dinner_total': {'mass': 0},
            'snacks': [],
            'snacks_total': {'mass': 0},
            'total_total': {'mass': 0}
        } for x in range(1, days_amount + 1)]

    for i, _ in enumerate(days):
        date = format_date(first_date, i + 1)
        day_meals = [x for x in meals_info if x['day_number'] == i + 1]
        days[i] = calculate_day_info(i + 1,  date, attendees_count, day_meals)

    return days


@bp.route('/')
def index():
    db = get_db()
    trips = db.execute(
        'SELECT id, name, from_date, till_date, last_update FROM trips WHERE archived=0'
    ).fetchall()
    return render_template('trips/trips.j2', trip_days=trips, no_trips=True if not trips else False)


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
        'SELECT id, name, from_date, till_date, attendees FROM trips WHERE id=?',
        (trip_id,)
    ).fetchone()

    meals_info = db.execute(
        "SELECT mr.id, mr.trip_id, mr.day_number, mr.meal_number, mr.product_id, mr.mass, p.name, p.calories, p.proteins, p.fats, p.carbs FROM 'meal_records' mr INNER JOIN 'products' p ON p.id=mr.product_id WHERE trip_id=?",
        (trip_id,)
    ).fetchall()
    
    first_date = trip_info['from_date']
    last_date = trip_info['till_date']
    days = calculate_total_days_info(first_date, last_date, trip_info['attendees'], meals_info)
    return render_template('trips/trip.j2', trip=trip_info, days=days)


@bp.route('/trips/trip/<int:trip_id>/day_table/<int:day_number>', methods=('POST',))
def day_tables(trip_id, day_number):
    db = get_db()

    trip_info = db.execute(
        'SELECT id, name, from_date, till_date, attendees FROM trips WHERE id=?',
        (trip_id,)
    ).fetchone()

    meals_info = db.execute(
        "SELECT mr.id, mr.trip_id, mr.day_number, mr.meal_number, mr.product_id, mr.mass, p.name, p.calories, p.proteins, p.fats, p.carbs FROM 'meal_records' mr INNER JOIN 'products' p ON p.id=mr.product_id WHERE trip_id=? AND day_number=?",
        (trip_id, day_number)
    ).fetchall()

    date = format_date(trip_info['from_date'], day_number)
    day = calculate_day_info(day_number, date, trip_info['attendees'], meals_info)
    day_macro = get_template_attribute('trips/trip_day.j2', 'day')
    return day_macro(day)

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
