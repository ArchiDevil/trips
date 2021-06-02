import functools
import hashlib
from collections import defaultdict

from flask import Blueprint, render_template, get_template_attribute, abort, g, url_for, redirect, request
from sqlalchemy.sql.expression import select

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, MealRecord, Product, AccessGroup, User
from organizer.strings import STRING_TABLE
from organizer.meals_utils import calculate_total_days_info, format_date, calculate_day_info

bp = Blueprint('meals', __name__, url_prefix='/meals')


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

    return render_template('meals/meals.html',
                           trip=trip, days=days)


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


@bp.route('cycle_days/<int:trip_id>', methods=['POST'])
@login_required_group(AccessGroup.TripManager)
def cycle_days(trip_id):
    if not 'src-start' in request.form or not 'src-end' in request.form:
        abort(400)

    if not 'dst-start' in request.form or not 'dst-end' in request.form:
        abort(400)

    try:
        src_start = int(request.form['src-start'])
        src_end = int(request.form['src-end'])
        dst_start = int(request.form['dst-start'])
        dst_end = int(request.form['dst-end'])
    except ValueError:
        abort(403)

    if src_start <= 0 or src_end <= 0 or dst_start <= 0 or dst_end <= 0:
        abort(403)

    if src_start > src_end or dst_start > dst_end:
        abort(403)

    # ranges are touching each other
    if src_start == dst_start or src_start == dst_end or src_end == dst_start or src_end == dst_end:
        abort(400)

    if dst_start > src_start and dst_start < src_end:
        abort(400)

    if dst_end > src_start and dst_end < src_end:
        abort(400)

    src_days_count = src_end - src_start + 1

    with get_session() as session:
        if 'overwrite' in request.form:
            session.query(MealRecord).filter(MealRecord.trip_id == trip_id,
                                             MealRecord.day_number >= dst_start,
                                             MealRecord.day_number <= dst_end).delete()
            session.commit()

        meals_info = session.query(MealRecord).filter(MealRecord.trip_id == trip_id,
                                                      MealRecord.day_number >= src_start,
                                                      MealRecord.day_number <= src_start + src_days_count).order_by(MealRecord.day_number).all()
        meals_per_day = defaultdict(list)
        for meal in meals_info:
            meals_per_day[meal.day_number - src_start].append(meal)

        trip_info = session.query(Trip).filter(Trip.id == trip_id).first()
        trip_duration = (trip_info.till_date - trip_info.from_date).days + 1

        if src_end > trip_duration or dst_end > trip_duration:
            abort(403)

        for day_number in range(dst_start, dst_end + 1):
            idx = (day_number - dst_start) % src_days_count
            for meal in meals_per_day[idx]:
                new_record = MealRecord(trip_id=trip_id,
                                        product_id=meal.product_id,
                                        day_number=day_number,
                                        meal_number=meal.meal_number,
                                        mass=meal.mass)
                session.add(new_record)
        session.commit()

    return redirect(url_for('meals.days_view', trip_id=trip_id))
