import datetime
from typing import List

from flask import Blueprint, render_template, request, url_for, redirect, get_template_attribute

from organizer.db import get_session
from organizer.schema import Trip, MealRecord, Product

bp = Blueprint('trips', __name__)


def format_date(first_day, current_day_number):
    y = (first_day + datetime.timedelta(days=current_day_number - 1)).year
    m = (first_day + datetime.timedelta(days=current_day_number - 1)).month
    d = (first_day + datetime.timedelta(days=current_day_number - 1)).day
    return '{:4}-{:02}-{:02}'.format(y, m, d)


def calculate_day_info(day_number: int,
                       date: str,
                       meals_info: List[dict]):
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
        meal_number = record.meal_number
        day[meals_map[meal_number]].append(
            {
                'id': record.id,
                'name': record.name,
                'mass': record.mass,
                'proteins': record.proteins * record.mass / 100.0,
                'fats': record.fats * record.mass / 100.0,
                'carbs': record.carbs * record.mass / 100.0,
                'cals': record.calories * record.mass / 100.0
            }
        )

    # calculating totals for each day
    for field in ('mass', 'proteins', 'fats', 'carbs', 'cals'):
        day['breakfast_total'][field] = sum(
            [e[field] for e in day['breakfast']])
        day['lunch_total'][field] = sum([e[field] for e in day['lunch']])
        day['dinner_total'][field] = sum([e[field] for e in day['dinner']])
        day['snacks_total'][field] = sum([e[field] for e in day['snacks']])

        day['total_total'][field] = sum([day['breakfast_total'][field],
                                         day['lunch_total'][field],
                                         day['dinner_total'][field],
                                         day['snacks_total'][field]])

    day['date'] = date
    return day


def calculate_total_days_info(first_date, last_date, meals_info):
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
        day_meals = [x for x in meals_info if x.day_number == i + 1]
        days[i] = calculate_day_info(i + 1, date, day_meals)

    return days


@bp.route('/')
def index():
    with get_session() as session:
        trips = session.query(Trip.id, Trip.name, Trip.from_date,
                              Trip.till_date).filter(Trip.archived == 0).all()
        return render_template('trips/trips.html', trip_days=trips, no_trips=bool(not trips))


@bp.route('/trips/add', methods=['GET', 'POST'])
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

        return redirect(url_for('trips.index'))
    return render_template('trips/add.html')


@bp.route('/trips/trip/<int:trip_id>')
def days_view(trip_id):
    with get_session() as session:
        trip_info = session.query(Trip).filter(Trip.id == trip_id).one()
        meals_info = session.query(MealRecord.id,
                                   MealRecord.trip_id,
                                   MealRecord.day_number,
                                   MealRecord.meal_number,
                                   MealRecord.mass,
                                   Product.name,
                                   Product.calories,
                                   Product.proteins,
                                   Product.fats,
                                   Product.carbs).join(Product).filter(Trip.id == trip_id).all()

    first_date = trip_info.from_date
    last_date = trip_info.till_date
    days = calculate_total_days_info(first_date, last_date, meals_info)
    return render_template('trips/trip.html', trip=trip_info, days=days)


@bp.route('/trips/trip/<int:trip_id>/day_table/<int:day_number>', methods=['POST'])
def day_tables(trip_id, day_number):
    with get_session() as session:
        trip_info = session.query(Trip).filter(Trip.id == trip_id).one()
        meals_info = session.query(MealRecord.id,
                                   MealRecord.trip_id,
                                   MealRecord.meal_number,
                                   MealRecord.product_id,
                                   MealRecord.mass,
                                   Product.name,
                                   Product.calories,
                                   Product.proteins,
                                   Product.fats,
                                   Product.carbs).join(Product).filter(Trip.id == trip_id, MealRecord.day_number == day_number).all()

    date = format_date(trip_info.from_date, day_number)
    day = calculate_day_info(day_number, date, meals_info)
    day_macro = get_template_attribute('trips/trip_day.html', 'day')
    return day_macro(day)


@bp.route('/trips/edit/<int:trip_id>', methods=['GET', 'POST'])
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
            return redirect(url_for('trips.days_view', trip_id=trip_id))

        trip_info = session.query(Trip).filter(Trip.id == trip_id).one()
    return render_template('trips/edit.html', trip=trip_info, action='edit')


@bp.route('/trips/archive/<int:trip_id>')
def archive(trip_id):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.id == trip_id).one()
        # TODO: what if no such trip?
        trip.archived = 1
        trip.last_update = datetime.datetime.utcnow()
        session.commit()
    return redirect(url_for('trips.index'))
