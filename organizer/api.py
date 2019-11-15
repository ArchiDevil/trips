import datetime

from flask import Blueprint, request, jsonify

from organizer.db import get_session
from organizer.schema import Product, Trip, MealRecord

products_bp = Blueprint('api.products', __name__, url_prefix='/api/v1/products')
meals_bp = Blueprint('api.meals', __name__, url_prefix='/api/v1/meals')


@products_bp.route('/search', methods=['GET'])
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
                                                            Product.archived == 0).limit(count).all()
        return {
            'result': True,
            'products': [{'id': prod.id, 'name': prod.name} for prod in found_products]
        }


@products_bp.route('/units', methods=['GET'])
def product_units():
    product_id = request.args['id']

    with get_session() as session:
        product = session.query(Product).filter(Product.id == product_id,
                                                Product.archived == 0).first()

        if not product:
            return {'result': False}

        # TODO: put these units in some table
        units = ['grams']
        if product.grams is not None:
            units.append('pcs')

        return {
            'result': True,
            'units': units
        }


@meals_bp.route('/add', methods=['POST'])
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
        assert unit in ['grams', 'pcs']
    except (ValueError, AssertionError):
        return {"result": False}

    product_id = request.form['product_id']
    with get_session() as session:
        found_product = session.query(Product.id,
                                      Product.grams).filter(Product.id == product_id,
                                                            Product.archived != 1).first()

        if not found_product:
            return {'result': False}

        grams = found_product.grams

        if grams is None:
            if unit != 'grams':
                return {'result': False}
        elif unit == 'pcs':
            mass = grams * mass

        meal_number = meals_map[meal_name]
        session.add(MealRecord(trip_id=trip_id,
                               product_id=found_product.id,
                               day_number=day_number,
                               meal_number=meal_number,
                               mass=mass))
        session.commit()

        # update the last time trip was touched
        session.query(Trip).filter(Trip.id == trip_id).update({'last_update': datetime.datetime.utcnow()})
        session.commit()
        return {'result': True}


@meals_bp.route('/remove', methods=['DELETE'])
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
        session.query(Trip).filter(Trip.id == meal_info.trip_id).update({'last_update': datetime.datetime.utcnow()})
        session.commit()
        return {'result': True}
