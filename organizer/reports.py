from flask import Blueprint, render_template

from organizer.db import get_db

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/shopping/<int:trip_id>')
def shopping(trip_id):
    db = get_db()
    trip = db.execute(
        'SELECT name, attendees FROM trips WHERE id=?',
        [trip_id]
    ).fetchone()

    meals = db.execute(
        "SELECT p.id, p.name, p.grams, mr.mass " \
        "FROM 'meal_records' mr "                \
        "INNER JOIN 'products' p "               \
        "ON p.id=mr.product_id "                 \
        "WHERE trip_id=?",
        [trip_id]
    ).fetchall()

    products = {}
    for meal in meals:
        if meal['id'] not in products.keys():
            products[meal['id']] = {'id': meal['id'], 'name': meal['name'], 'mass': 0}
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
