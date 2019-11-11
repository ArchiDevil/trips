from flask import Blueprint, render_template, abort, request

from organizer.db import get_db

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/shopping/<int:trip_id>')
def shopping(trip_id):
    db = get_db()
    trip = db.execute(
        'SELECT name, attendees FROM trips WHERE id=?',
        [trip_id]
    ).fetchone()

    if not trip:
        abort(404)

    meals = db.execute(
        "SELECT p.id, p.name, p.grams, mr.mass "
        "FROM 'meal_records' mr "
        "INNER JOIN 'products' p "
        "ON p.id=mr.product_id "
        "WHERE trip_id=?",
        [trip_id]
    ).fetchall()

    products = {}
    for meal in meals:
        if meal['id'] not in products.keys():
            products[meal['id']] = {'id': meal['id'],
                                    'name': meal['name'], 'mass': 0}
            if meal['grams'] is not None:
                products[meal['id']]['pieces'] = 0
        products[meal['id']]['mass'] += meal['mass']

        if meal['grams'] is not None:
            # TODO: this will lead to floating error, so do something with it
            products[meal['id']]['pieces'] += meal['mass'] / meal['grams']

    for product in products.values():
        product['mass'] *= trip['attendees']
        if 'pieces' in product.keys():
            product['pieces'] *= trip['attendees']

    return render_template('reports/shopping.html', trip=trip, products=products)


@bp.route('/packing/<int:trip_id>')
def packing(trip_id):
    # four is a default value that is suitable for the most cases
    return packing_ext(trip_id, 4)


@bp.route('/packing/<int:trip_id>/<int:columns_count>')
def packing_ext(trip_id, columns_count):
    db = get_db()
    trip = db.execute(
        'SELECT id, name, attendees FROM trips WHERE id=?',
        [trip_id]
    ).fetchone()

    if not trip:
        abort(404)

    meals = db.execute(
        'SELECT m.day_number, m.meal_number, p.name, m.mass '
        'FROM meal_records m '
        'INNER JOIN products p '
        'WHERE p.id = m.product_id AND m.trip_id=?',
        [trip_id]
    ).fetchall()

    if not meals:
        abort(500)

    products = {}
    for meal in meals:
        day = meal['day_number']
        if day not in products.keys():
            products[day] = []

        products[day].append({
            'name': meal['name'],
            'meal_number': meal['meal_number'],
            'mass': meal['mass'] * trip['attendees'],
        })

    for arr in products.values():
        arr.sort(key=lambda x: x['meal_number'])

    return render_template('reports/packing.html', trip=trip, products=products, columns_count=columns_count)
