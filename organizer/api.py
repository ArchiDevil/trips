import datetime
import functools
from enum import Enum
from typing import List, Dict, Tuple, Any

from flask import Blueprint, request, g, abort

from organizer.db import get_session
from organizer.schema import Product, Trip, MealRecord, AccessGroup
from organizer.meals_utils import calculate_total_days_info

products_bp = Blueprint('api.products', __name__, url_prefix='/api/v1/products')
meals_bp = Blueprint('api.meals', __name__, url_prefix='/api/v1/meals')


def api_login_required_group(group=None):
    def api_login_required_grouped(view):
        @functools.wraps(view)
        def api_wrapped_view_grouped(**kwargs):
            if 'user' not in g or g.user is None:
                abort(403)
            if group and g.user.access_group.value < group.value:
                abort(403)
            return view(**kwargs)
        return api_wrapped_view_grouped
    return api_login_required_grouped


@products_bp.route('/search', methods=['GET'])
@api_login_required_group()
def products_search():
    # TODO: check the provided name
    search_request = request.args['name']
    search_request = "%{}%".format(search_request)

    count = request.args['count']
    try:
        count = int(count)
    except ValueError:
        return {'result': False}

    with get_session() as session:
        found_products = session.query(Product.id,
                                       Product.name).filter(Product.name.ilike(search_request),
                                                            Product.archived == False).limit(count).all()
        return {
            'result': True,
            'products': [{'id': prod.id, 'name': prod.name} for prod in found_products]
        }


class Units(Enum):
    Grams = 0
    Pieces = 1


@products_bp.route('/units', methods=['GET'])
@api_login_required_group()
def product_units():
    product_id = request.args['id']

    with get_session() as session:
        product = session.query(Product).filter(Product.id == product_id,
                                                Product.archived == False).first()

        if not product:
            return {'result': False}

        # TODO: put these units in some table
        units = [Units.Grams.value]
        if product.grams is not None:
            units.append(Units.Pieces.value)

        return {
            'result': True,
            'units': units
        }


@meals_bp.route('/add', methods=['POST'])
@api_login_required_group(AccessGroup.TripManager)
def meals_add():
    trip_id = request.form['trip_id']
    meal_name = request.form['meal_name']
    day_number = request.form['day_number']
    mass = request.form['mass']
    unit = request.form['unit']

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
            assert session.query(Trip.id).filter(Trip.id == trip_id).first()

            trip_info = session.query(Trip.from_date,
                                      Trip.till_date).filter(Trip.id == trip_id).one()
            diff = trip_info.till_date - trip_info.from_date

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

    product_id = request.form['product_id']
    with get_session() as session:
        found_product = session.query(Product.id,
                                      Product.grams).filter(Product.id == product_id,
                                                            Product.archived == False).first()

        if not found_product:
            return {'result': False}

        grams = found_product.grams

        if grams is None:
            if unit != Units.Grams.value:
                return {'result': False}
        elif unit == Units.Pieces.value:
            mass = grams * mass

        meal_number = meals_map[meal_name]

        existing_record: MealRecord = session.query(MealRecord).filter(MealRecord.trip_id == trip_id,
                                                                       MealRecord.product_id == found_product.id,
                                                                       MealRecord.day_number == day_number,
                                                                       MealRecord.meal_number == meal_number).first()
        if existing_record:
            existing_record.mass += mass
        else:
            session.add(MealRecord(trip_id=trip_id,
                                   product_id=found_product.id,
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


@meals_bp.route('/remove', methods=['DELETE'])
@api_login_required_group(AccessGroup.TripManager)
def meals_remove():
    meal_id = request.form['meal_id']

    try:
        meal_id = int(meal_id)
        assert meal_id > 0
    except (ValueError, AssertionError):
        return {'result': False}

    with get_session() as session:
        meal_info = session.query(MealRecord.trip_id).filter(
            MealRecord.id == meal_id).first()
        if not meal_info:
            return {'result': False}

        session.query(MealRecord).filter(MealRecord.id == meal_id).delete()
        session.commit()

        # update the last time trip was touched
        session.query(Trip).filter(Trip.id == meal_info.trip_id).update({
            'last_update': datetime.datetime.utcnow()
        })
        session.commit()
        return {'result': True}


def calculate_averages(days: List[Dict[str, Any]]) -> Tuple[int, int]:
    full_mass = 0
    full_cals = 0
    for day in days:
        full_mass += day['total_total']['mass']
        full_cals += day['total_total']['cals']

    return full_mass // len(days), full_cals // len(days)


@meals_bp.route('/averages', methods=['GET'])
@api_login_required_group()
def meals_averages():
    if not 'trip_id' in request.args:
        abort(400)

    trip_id = request.args['trip_id']

    with get_session() as session:
        trip_info: Trip = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip_info:
            abort(404)

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

    first_date = trip_info.from_date
    last_date = trip_info.till_date
    days = calculate_total_days_info(first_date, last_date, meals_info)
    mass, cals = calculate_averages(days)

    return {
        'mass': mass,
        'cals': cals
    }
