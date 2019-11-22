from flask import Blueprint, render_template, abort, redirect, url_for

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, Product, MealRecord, AccessGroup

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/shopping/<int:trip_id>')
@login_required_group(AccessGroup.Guest)
def shopping(trip_id):
    with get_session() as session:
        trip = session.query(Trip.name, Trip.attendees).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        meals = session.query(MealRecord.mass,
                              Product.id,
                              Product.name,
                              Product.grams).join(Product).filter(MealRecord.trip_id == trip_id).all()

    products = {}
    for meal in meals:
        if meal.id not in products.keys():
            products[meal.id] = {
                'id': meal.id,
                'name': meal.name,
                'mass': 0
            }
            if meal.grams is not None:
                products[meal.id]['pieces'] = 0

        products[meal.id]['mass'] += meal.mass * trip.attendees

        if meal.grams is not None:
            products[meal.id]['pieces'] += meal.mass * trip.attendees / meal.grams

    return render_template('reports/shopping.html', trip=trip, products=products)


@bp.route('/packing/<int:trip_id>')
@login_required_group(AccessGroup.Guest)
def packing(trip_id):
    # four is a default value that is suitable for the most cases
    return redirect(url_for('reports.packing_ext', trip_id=trip_id, columns_count=4))


@bp.route('/packing/<int:trip_id>/<int:columns_count>')
@login_required_group(AccessGroup.Guest)
def packing_ext(trip_id, columns_count):
    if columns_count > 6 or columns_count < 1:
        abort(403)

    with get_session() as session:
        trip = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        meals = session.query(MealRecord.day_number,
                              MealRecord.meal_number,
                              MealRecord.mass,
                              Product.name).join(Product).filter(MealRecord.trip_id == trip_id).all()

    products = {}
    for meal in meals:
        day = meal.day_number
        if day not in products.keys():
            products[day] = []

        products[day].append({
            'name': meal.name,
            'meal_number': meal.meal_number,
            'mass': meal.mass * trip.attendees,
        })

    for arr in products.values():
        arr.sort(key=lambda x: x['meal_number'])

    return render_template('reports/packing.html', trip=trip, products=products, columns_count=columns_count)
