import datetime

from flask import Blueprint, request, jsonify

from organizer.db import get_session
from organizer.schema import Product, Trip, MealRecord

products_bp = Blueprint('api.products', __name__, url_prefix='/api/v1/products')
meals_bp = Blueprint('api.meals', __name__, url_prefix='/api/v1/meals')


@products_bp.route('/search', methods=['POST'])
def products_search():
    # TODO: check the provided name
    search_request = request.form['name']
    search_request = "%{}%".format(search_request)

    count = request.form['count']
    # TODO: check if it is wrong
    count = int(count)

    with get_session() as session:
        found_products = session.query(Product.id, Product.name).filter(
            Product.name.ilike(search_request), Product.archived == 0).limit(count).all()
        output = []
        for data in found_products:
            output.append({'id': data.id, 'name': data.name})
        return jsonify(output)


@products_bp.route('/units', methods=['POST'])
def product_units():
    # TODO: check the id
    product_id = request.form['id']

    with get_session() as session:
        product = session.query(Product).filter(
            Product.id == product_id, Product.archived == 0).one()

        if not product:
            return jsonify({
                'result': False
            })

        # TODO: put these units in some table
        units = ['grams']
        if product.grams is not None:
            units.append('pcs')

        return jsonify({
            'result': True,
            'units': units
        })


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
        assert meal_name in meals_map
        day_number = int(day_number)
        assert day_number > 0
        mass = int(mass)
        assert mass > 0
        assert unit in ['grams', 'pcs']
    except:
        return jsonify({"result": False})

    product_id = request.form['product_id']
    with get_session() as session:
        found_product = session.query(Product.id, Product.grams).filter(
            Product.id == product_id, Product.archived != 1).one()

        if not found_product:
            return jsonify({'result': False})

        grams = found_product.grams

        if grams is None:
            if unit != 'grams':
                return jsonify({'result': False})
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
        return jsonify({'result': True})


@meals_bp.route('/remove', methods=['POST'])
def meals_remove():
    meal_id = request.form['meal_id']

    try:
        meal_id = int(meal_id)
        assert meal_id > 0
    except:
        return jsonify({'result': False})

    with get_session() as session:
        meal_info = session.query(MealRecord.trip_id).filter(MealRecord.id == meal_id).one()
        # TODO: what if None?

        session.query(MealRecord).filter(MealRecord.id == meal_id).delete()
        session.commit()

        # update the last time trip was touched
        session.query(Trip).filter(Trip.id == meal_info.trip_id).update({'last_update': datetime.datetime.utcnow()})
        session.commit()
    return jsonify({'result': True})
