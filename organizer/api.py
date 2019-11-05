from flask import Blueprint, request, jsonify

from organizer.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/products/search', methods=['POST'])
def products_search():
    # TODO: check the provided name
    search_request = request.form['name']
    search_request = "%{}%".format(search_request)

    count = request.form['count']
    count = int(count)

    db = get_db()
    found_products = db.execute(
        "SELECT id, name FROM products WHERE name LIKE ? AND archived=0 LIMIT ?",
        [search_request, count]
    ).fetchall()

    output = []
    for data in found_products:
        output.append({'id': data['id'], 'name': data['name']})
    return jsonify(output)


@bp.route('/products/units', methods=['POST'])
def product_units():
    product_id = request.form['id']
    db = get_db()
    product = db.execute(
        "SELECT grams FROM products WHERE id=? AND archived=0",
        [product_id]
    ).fetchone()
    
    if not product:
        return jsonify({
            'result': False
        })

    units = ['g']
    if product['grams'] is not None:
        units.append('p')

    return jsonify({
        'result': True,
        'units': units
    })


@bp.route('/meals/add', methods=['POST'])
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
        assert unit in ['g', 'p']
    except:
        return jsonify({"result": False})

    product_name = request.form['name']
    db = get_db()
    found_products = db.execute(
        "SELECT id, grams FROM products WHERE name=? AND NOT archived=1",
        [product_name]
    ).fetchone()

    if not found_products:
        return jsonify({'result': False})

    product_id = found_products['id']
    grams = found_products['grams']
    if grams is None:
        # if product has no special units it must use grams
        assert unit == 'g'
    elif unit == 'p':
        mass = grams * mass

    meal_number = meals_map[meal_name]
    db.execute(
        "INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (?, ?, ?, ?, ?)",
        [trip_id, day_number, meal_number, product_id, mass]
    )
    db.commit()
    return jsonify({'result': True})


@bp.route('/meals/remove', methods=['POST'])
def meals_remove():
    meal_id = request.form['meal_id']

    try:
        meal_id = int(meal_id)
        assert meal_id > 0
    except:
        return jsonify({'result': False})

    db = get_db()
    db.execute(
        'DELETE FROM meal_records WHERE id=?',
        [meal_id]
    )
    db.commit()
    return jsonify({'result': True})
