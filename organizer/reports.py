from collections import defaultdict

from sqlalchemy.sql import func
from flask import Blueprint, render_template, abort, redirect, url_for

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Trip, Product, MealRecord, AccessGroup, Group

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.get('/shopping/<int:trip_id>')
@login_required_group(AccessGroup.Guest)
def shopping(trip_id):
    with get_session() as session:
        trip = session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            abort(404)

        persons_count = session.query(func.sum(Group.persons)).filter(Group.trip_id == trip_id).scalar()
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

        products[meal.id]['mass'] += meal.mass * persons_count

        if meal.grams is not None:
            products[meal.id]['pieces'] += meal.mass * persons_count / meal.grams

    # sort products by name
    products = [x for x in products.values()]
    products.sort(key=lambda x: x['name'])
    return render_template('reports/shopping.html', trip=trip, products=products)


@bp.get('/packing/<int:trip_id>')
@login_required_group(AccessGroup.Guest)
def packing(trip_id):
    # four is a default value that is suitable for the most cases
    return redirect(url_for('reports.packing_ext', trip_id=trip_id, columns_count=4))


@bp.get('/packing/<int:trip_id>/<int:columns_count>')
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
                              Product.name,
                              Product.grams).join(Product).filter(MealRecord.trip_id == trip_id).order_by(MealRecord.day_number).all()

        trip_groups = session.query(Group.persons).distinct().filter(Group.trip_id == trip_id).all()
        person_groups = [group.persons for group in trip_groups]

    products = defaultdict(list)
    for meal in meals:
        day = meal.day_number
        products[day].append({
            'name': meal.name,
            'meal_number': meal.meal_number,
            'mass': [meal.mass * persons for persons in person_groups],
        })

        if meal.grams is not None:
            products[day][-1]['grams'] = meal.grams

    for arr in products.values():
        arr.sort(key=lambda x: x['meal_number'])

    return render_template('reports/packing.html', trip=trip,
                           products=products, columns_count=columns_count,
                           person_groups=person_groups)
