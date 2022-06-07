import datetime
from typing import Optional, Dict, Any

from flask import Blueprint, abort, request, url_for, g

from organizer.auth import api_login_required_group, user_has_trip_access
from organizer.db import get_session
from organizer.schema import AccessGroup, Trip, MealRecord, Product, \
                             TripAccessType, Units

BP = Blueprint('meals', __name__, url_prefix='/meals')

def format_date(first_day: datetime.date, current_day_number: int):
    return (first_day + datetime.timedelta(days=current_day_number - 1)).strftime('%d/%m')


@BP.post('/add')
@api_login_required_group(AccessGroup.User)
def meals_add():
    json: Dict[str, Any] = request.json
    trip_id = json['trip_id']
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
        trip_id = int(trip_id)
        assert trip_id > 0
        with get_session() as session:
            trip = session.query(Trip).filter(Trip.id == trip_id).first()
            assert trip

            if not user_has_trip_access(trip,
                                        g.user.id,
                                        g.user.access_group == AccessGroup.Administrator,
                                        session,
                                        TripAccessType.Write):
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

        existing_record: MealRecord = session.query(MealRecord).filter(MealRecord.trip_id == trip_id,
                                                                       MealRecord.product_id == product.id,
                                                                       MealRecord.day_number == day_number,
                                                                       MealRecord.meal_number == meal_number).first()
        if existing_record:
            existing_record.mass += mass
        else:
            session.add(MealRecord(trip_id=trip_id,
                                   product_id=product.id,
                                   day_number=day_number,
                                   meal_number=meal_number,
                                   mass=mass))
        session.commit()

        # update the last time trip was touched
        session.query(Trip).filter(Trip.id == trip_id).update({
            'last_update': datetime.datetime.utcnow()
        })
        session.commit()
        return {'result': True}


@BP.delete('/remove')
@api_login_required_group(AccessGroup.User)
def meals_remove():
    if not 'meal_id' in request.json:
        abort(400)

    try:
        meal_id = int(request.json['meal_id'])
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
                                    session,
                                    TripAccessType.Write):
            abort(403)

        session.query(MealRecord).filter(MealRecord.id == meal_id).delete()
        session.commit()

        session.query(Trip).filter(Trip.id == meal_info.trip_id).update({
            'last_update': datetime.datetime.utcnow()
        })
        session.commit()
        return {'result': True}


@BP.post('/clear')
@api_login_required_group(AccessGroup.User)
def meals_clear():
    json: Any = request.json
    if not 'trip_id' in json or not 'day_number' in json:
        abort(400)

    try:
        trip_id = int(json['trip_id'])
        day_number = int(json['day_number'])
    except ValueError:
        abort(400)

    with get_session() as session:
        trip: Optional[Trip] = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        if not user_has_trip_access(trip,
                                    g.user.id,
                                    g.user.access_group == AccessGroup.Administrator,
                                    session,
                                    TripAccessType.Write):
            abort(403)

        session.query(MealRecord).filter(MealRecord.trip_id == trip_id,
                                         MealRecord.day_number == day_number).delete()
        trip.last_update = datetime.datetime.utcnow()
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

        output = {}
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


@BP.get('/<int:trip_id>')
@api_login_required_group(AccessGroup.User)
def get_meals(trip_id: int):
    with get_session() as session:
        trip: Optional[Trip] = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        if not user_has_trip_access(trip,
                                    g.user.id,
                                    g.user.access_group == AccessGroup.Administrator,
                                    session,
                                    TripAccessType.Read):
            abort(403)

        days_count: int = (trip.till_date - trip.from_date).days + 1

    days = [
        {
            'number': i + 1,
            'date': format_date(trip.from_date, i + 1),
            'meals': extract_meals(trip_id, i + 1),
            'reload_link': url_for('api.meals.get_day_meals', trip_id=trip_id, day_number=i + 1)
        } for i in range(days_count)
    ]
    return {'days': days}


@BP.get('/<int:trip_id>/<int:day_number>')
@api_login_required_group(AccessGroup.User)
def get_day_meals(trip_id: int, day_number: int):
    with get_session() as session:
        trip: Optional[Trip] = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        days_count: int = (trip.till_date - trip.from_date).days + 1
        if day_number > days_count or day_number < 1:
            abort(404)

        if not user_has_trip_access(trip,
                                    g.user.id,
                                    g.user.access_group == AccessGroup.Administrator,
                                    session,
                                    TripAccessType.Read):
            abort(403)

        return {'day': {
            'number': day_number,
            'date': format_date(trip.from_date, day_number),
            'meals': extract_meals(trip_id, day_number),
            'reload_link': url_for('api.meals.get_day_meals', trip_id=trip_id, day_number=day_number)
        }}
