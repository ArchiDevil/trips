import datetime
import functools
import hashlib
from typing import List

from flask import Blueprint, render_template, get_template_attribute, abort, g

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, MealRecord, Product, AccessGroup, User
from organizer.strings import STRING_TABLE

bp = Blueprint('meals', __name__, url_prefix='/meals')


def format_date(first_day, current_day_number):
    return (first_day + datetime.timedelta(days=current_day_number - 1)).strftime('%d/%m')


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
        day[meals_map[meal_number]].append({
            'id': record.id,
            'name': record.name,
            'mass': record.mass,
            'proteins': record.proteins * record.mass / 100.0,
            'fats': record.fats * record.mass / 100.0,
            'carbs': record.carbs * record.mass / 100.0,
            'cals': record.calories * record.mass / 100.0
        })

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


def calculate_total_days_info(first_date, last_date, meals_info):
    days_amount = (last_date - first_date).days + 1
    days = [{
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


@bp.route('/<int:trip_id>')
@login_required_group(AccessGroup.Guest)
def days_view(trip_id):
    with get_session() as session:
        trip_info: Trip = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip_info:
            abort(404)

        if trip_info.created_by != g.user.id:
            user = session.query(User).filter(User.id == g.user.id).one()
            if not trip_info in user.shared_trips:
                user.shared_trips.append(trip_info)
                session.commit()

        meals_info = session.query(MealRecord.id,
                                   MealRecord.trip_id,
                                   MealRecord.day_number,
                                   MealRecord.meal_number,
                                   MealRecord.mass,
                                   Product.name,
                                   Product.calories,
                                   Product.proteins,
                                   Product.fats,
                                   Product.carbs).join(Product).filter(MealRecord.trip_id == trip_id).all()
        trip_info = session.query(Trip).filter(Trip.id == trip_id).first()

        trip = {
            'id': trip_info.id,
            'name': trip_info.name,
            'from_date': trip_info.from_date,
            'till_date': trip_info.till_date,
            'attendees': functools.reduce(lambda x, y: x+y, [group.persons for group in trip_info.groups]),
            'magic':  int(hashlib.sha1(trip_info.name.encode()).hexdigest(), 16) % 8 + 1
        }

    first_date = trip_info.from_date
    last_date = trip_info.till_date
    days = calculate_total_days_info(first_date, last_date, meals_info)

    return render_template('meals/meals.html', trip=trip, days=days)


@bp.route('/<int:trip_id>/day_table/<int:day_number>')
@login_required_group(AccessGroup.Guest)
def day_tables(trip_id, day_number):
    with get_session() as session:
        trip_info = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip_info:
            abort(404)

        if (trip_info.till_date - trip_info.from_date).days + 1 < day_number:
            abort(404)

        meals_info = session.query(MealRecord.id,
                                   MealRecord.trip_id,
                                   MealRecord.meal_number,
                                   MealRecord.product_id,
                                   MealRecord.mass,
                                   Product.name,
                                   Product.calories,
                                   Product.proteins,
                                   Product.fats,
                                   Product.carbs).join(Product).filter(MealRecord.trip_id == trip_id,
                                                                       MealRecord.day_number == day_number).all()

    date = format_date(trip_info.from_date, day_number)
    day = calculate_day_info(day_number, date, meals_info)
    day_macro = get_template_attribute('meals/meals_day.html', 'day')
    return day_macro(day, string_table=STRING_TABLE)
