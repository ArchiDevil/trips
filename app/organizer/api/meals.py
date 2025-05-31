from collections import defaultdict
from datetime import datetime, date, timedelta, timezone
from typing import Any

from flask import Blueprint, abort, request, url_for, g
from sqlalchemy import update

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import AccessGroup, Trip, MealRecord, Product, Units
from organizer.utils.auth import user_has_trip_access

BP = Blueprint('meals', __name__, url_prefix='/meals')


def format_date(first_day: date, current_day_number: int):
    return (first_day + timedelta(days=current_day_number - 1)).strftime('%d/%m')


@BP.post('/add')
@api_login_required_group(AccessGroup.User)
def meals_add():
    json: dict[str, Any] = request.json # type: ignore
    trip_uid = json['trip_uid']
    meal_name = json['meal_name']
    day_number = json['day_number']
    mass = json['mass']
    unit = json['unit']

    # TODO: this is awful
    meals_map = {
        'breakfast': 0,
        'lunch': 1,
        'dinner': 2,
        'snacks': 3
    }

    try:
        assert trip_uid
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
            assert trip

            if not user_has_trip_access(trip,
                                        g.user.id,
                                        g.user.access_group == AccessGroup.Administrator,
                                        session):
                abort(403)

            diff = trip.till_date - trip.from_date
            day_number = int(day_number)
            assert day_number > 0
            assert day_number <= diff.days + 1

        assert meal_name in meals_map

        mass = int(mass)
        assert mass > 0

        unit = int(unit)
        assert unit in [x.value for x in Units]
    except (ValueError, AssertionError):
        return {"result": False}

    product_id = json['product_id']
    with get_session() as session:
        product = session.query(Product.id,
                                Product.grams).filter(Product.id == product_id,
                                                      Product.archived == False).first()

        if not product:
            return {'result': False}

        grams = product.grams

        if grams is None:
            if unit != Units.GRAMMS.value:
                return {'result': False}
        elif unit == Units.PIECES.value:
            mass = grams * mass

        meal_number = meals_map[meal_name]

        existing_record = session.query(MealRecord).filter(MealRecord.trip_id == trip.id,
                                                           MealRecord.product_id == product.id,
                                                           MealRecord.day_number == day_number,
                                                           MealRecord.meal_number == meal_number).first()
        if existing_record:
            existing_record.mass += mass
        else:
            session.add(MealRecord(trip_id=trip.id,
                                   product_id=product.id,
                                   day_number=day_number,
                                   meal_number=meal_number,
                                   mass=mass))
        session.commit()

        # update the last time trip was touched
        session.execute(
            update(Trip)
            .where(Trip.id == trip.id)
            .values(last_update=datetime.now(timezone.utc))
        )
        session.commit()
        return {'result': True}


@BP.delete('/remove')
@api_login_required_group(AccessGroup.User)
def meals_remove():
    if 'meal_id' not in request.json: # type: ignore
        abort(400)

    try:
        meal_id = int(request.json['meal_id']) # type: ignore
    except ValueError:
        abort(400)

    with get_session() as session:
        meal_info = session.query(MealRecord.trip_id).filter(MealRecord.id == meal_id).first()
        if not meal_info:
            return {'result': False}

        trip = session.query(Trip).filter(Trip.id == meal_info.trip_id).first()
        if not trip:
            abort(400)

        if not user_has_trip_access(trip,
                                    g.user.id,
                                    g.user.access_group == AccessGroup.Administrator,
                                    session):
            abort(403)

        session.query(MealRecord).filter(MealRecord.id == meal_id).delete()
        session.commit()

        trip.last_update = datetime.now(timezone.utc)
        session.commit()
        return {'result': True}


@BP.post('/clear')
@api_login_required_group(AccessGroup.User)
def meals_clear():
    json: Any = request.json
    if 'trip_uid' not in json or 'day_number' not in json:
        abort(400)

    try:
        trip_uid = json['trip_uid']
        day_number = int(json['day_number'])
    except ValueError:
        abort(400)

    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        if not user_has_trip_access(trip,
                                    g.user.id,
                                    g.user.access_group == AccessGroup.Administrator,
                                    session):
            abort(403)

        session.query(MealRecord).filter(MealRecord.trip_id == trip.id,
                                         MealRecord.day_number == day_number).delete()
        trip.last_update = datetime.now(timezone.utc)
        session.commit()

    return {'result': True}


def extract_meals(trip_id: int, day_number: int):
    with get_session() as session:
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
        meals_map = {
            0: 'breakfast',
            1: 'lunch',
            2: 'dinner',
            3: 'snacks'
        }

        output: dict[str, list[Any]] = {}
        for val in meals_map.values():
            output[val] = []

        for meal_info in meals_info:
            meal_record = {
                'id': meal_info.id,
                'name': meal_info.name,
                'mass': meal_info.mass,
                'calories': meal_info.calories * meal_info.mass / 100.0,
                'proteins': meal_info.proteins * meal_info.mass / 100.0,
                'fats': meal_info.fats * meal_info.mass / 100.0,
                'carbs': meal_info.carbs * meal_info.mass / 100.0
            }
            output[meals_map[meal_info.meal_number]].append(meal_record)
        return output


@BP.get('/<trip_uid>')
@api_login_required_group(AccessGroup.User)
def get_meals(trip_uid: str):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        days_count = (trip.till_date - trip.from_date).days + 1

    days = [
        {
            'number': i + 1,
            'date': format_date(trip.from_date, i + 1),
            'meals': extract_meals(trip.id, i + 1),
            'reload_link': url_for('api.meals.get_day_meals', trip_uid=trip.uid, day_number=i + 1)
        } for i in range(days_count)
    ]
    return {'days': days}


@BP.get('/<trip_uid>/<int:day_number>')
@api_login_required_group(AccessGroup.User)
def get_day_meals(trip_uid: str, day_number: int):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            abort(404)

        days_count = (trip.till_date - trip.from_date).days + 1
        if day_number > days_count or day_number < 1:
            abort(404)

        return {
            'day': {
                'number': day_number,
                'date': format_date(trip.from_date, day_number),
                'meals': extract_meals(trip.id, day_number),
                'reload_link': url_for('api.meals.get_day_meals', trip_uid=trip.uid, day_number=day_number)
            }
        }


@BP.post('/<trip_uid>/cycle')
@api_login_required_group(AccessGroup.User)
def cycle(trip_uid: str):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            return abort(404)

        if not user_has_trip_access(trip,
                                    g.user.id,
                                    g.user.access_group == AccessGroup.Administrator,
                                    session):
            return abort(403)

    data = request.json
    if not data:
        return abort(400)

    if 'src-start' not in data or 'src-end' not in data:
        return abort(400)

    if 'dst-start' not in data or 'dst-end' not in data:
        return abort(400)

    try:
        src_start = int(data['src-start'])
        src_end = int(data['src-end'])
        dst_start = int(data['dst-start'])
        dst_end = int(data['dst-end'])
    except ValueError:
        return abort(400)

    if src_start <= 0 or src_end <= 0 or dst_start <= 0 or dst_end <= 0:
        return abort(400)

    if src_start > src_end or dst_start > dst_end:
        return abort(400)

    # ranges are touching each other
    if src_start == dst_start or src_start == dst_end or src_end == dst_start or src_end == dst_end:
        return abort(400)

    if dst_start > src_start and dst_start < src_end:
        return abort(400)

    if dst_end > src_start and dst_end < src_end:
        return abort(400)

    src_days_count = src_end - src_start + 1

    with get_session() as session:
        if 'overwrite' in data and data['overwrite'] is True:
            session.query(MealRecord).filter(MealRecord.trip_id == trip.id,
                                             MealRecord.day_number >= dst_start,
                                             MealRecord.day_number <= dst_end).delete()
            session.commit()

        meals_info = session.query(MealRecord).filter(
            MealRecord.trip_id == trip.id,
            MealRecord.day_number >= src_start,
            MealRecord.day_number <= src_start + src_days_count).order_by(
                MealRecord.day_number).all()

        meals_per_day = defaultdict(list)
        for meal in meals_info:
            meals_per_day[meal.day_number - src_start].append(meal)

        trip_duration = (trip.till_date - trip.from_date).days + 1

        if src_end > trip_duration or dst_end > trip_duration:
            return abort(400)

        for day_number in range(dst_start, dst_end + 1):
            idx = (day_number - dst_start) % src_days_count
            for meal in meals_per_day[idx]:
                new_record = MealRecord(trip_id=trip.id,
                                        product_id=meal.product_id,
                                        day_number=day_number,
                                        meal_number=meal.meal_number,
                                        mass=meal.mass)
                session.add(new_record)
        session.commit()

    return {
        'result': 'ok'
    }
