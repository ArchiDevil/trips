import math
from typing import Final

from flask import Blueprint, request, url_for, abort
from sentry_sdk import capture_exception
from sqlalchemy import select, func

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import Product, Units, AccessGroup
from organizer.strings import STRING_TABLE


BP = Blueprint('products', __name__, url_prefix='/products')


def check_input_data(json_data: dict):
    name = str(json_data['name'])
    if not name or len(name) > 100:
        raise RuntimeError(STRING_TABLE['Products error incorrect name'])

    try:
        calories = float(json_data['calories'])
        if calories < 0 or math.isnan(calories):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect calories'])

    try:
        proteins = float(json_data['proteins'])
        if not (proteins >= 0 and proteins <= 100):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect proteins'])

    try:
        fats = float(json_data['fats'])
        if not (fats >= 0 and fats <= 100):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect fats'])

    try:
        carbs = float(json_data['carbs'])
        if not (carbs >= 0 and carbs <= 100):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect carbs'])

    grams = None
    if 'grams' in json_data:
        try:
            grams = float(json_data['grams'])
            if grams < 0 or math.isnan(grams):
                raise ValueError
        except ValueError:
            raise RuntimeError(STRING_TABLE['Products error incorrect grams'])


@BP.get('/search')
@api_login_required_group(AccessGroup.User)
def search():
    products_per_page: Final = 10
    page = int(request.args.get('page', 0))
    search_request = request.args.get('search', '')

    with get_session() as session:
        products_selector = select(Product).where(Product.archived == False)
        products_count_selector = select(func.count()).select_from(Product).where(Product.archived == False)

        if search_request:
            search_pattern = Product.name.ilike(f"%{search_request}%")
            products_selector = products_selector.where(search_pattern)
            products_count_selector = products_count_selector.where(search_pattern)

        products = session.execute(
            products_selector
            .order_by(Product.id)
            .offset(page * products_per_page)
            .limit(products_per_page)
        ).scalars()
        products_count = session.execute(products_count_selector).scalar_one()

        return {
            'page': page,
            'products_per_page': products_per_page,
            'total_count': products_count,
            'products': [
                {
                    'id': product.id,
                    'name': product.name,
                    'calories': product.calories,
                    'proteins': product.proteins,
                    'fats': product.fats,
                    'carbs': product.carbs,
                    'grams': product.grams,
                    'edit_link': url_for('api.products.edit', product_id=product.id),
                    'archive_link': url_for('api.products.archive', product_id=product.id)
                } for product in products
            ]
        }


@BP.get('/units')
@api_login_required_group(AccessGroup.User)
def product_units():
    product_id = request.args['id']

    with get_session() as session:
        product = session.query(Product).filter(Product.id == product_id,
                                                Product.archived == False).first()

        if not product:
            return {'result': False}

        # TODO: put these units in some table
        units = [Units.GRAMMS.value]
        if product.grams is not None:
            units.append(Units.PIECES.value)

        return {
            'result': True,
            'units': units
        }


@BP.post('/add')
@api_login_required_group(AccessGroup.User)
def add():
    data = request.json
    if not data:
        abort(400)

    try:
        check_input_data(data)
    except RuntimeError as exc:
        capture_exception(exc)
        return {
            'result': False,
            'error': str(exc)
        }

    name = data['name']
    calories = data['calories']
    proteins = data['proteins']
    fats = data['fats']
    carbs = data['carbs']

    grams = None
    if 'grams' in data:
        grams = data['grams']

    with get_session() as session:
        prod = Product(name=name, calories=calories,
                       proteins=proteins, fats=fats,
                       carbs=carbs, grams=grams)
        session.add(prod)
        session.commit()

    return {
        'result': True
    }


@BP.post('/<int:product_id>/edit')
@api_login_required_group(AccessGroup.Administrator)
def edit(product_id: int):
    data = request.json
    if not data:
        abort(400)

    try:
        check_input_data(data)
    except RuntimeError as exc:
        capture_exception(exc)
        return {
            'result': False,
            'error': str(exc)
        }

    name = data['name']
    calories = data['calories']
    proteins = data['proteins']
    fats = data['fats']
    carbs = data['carbs']

    grams = None
    if 'grams' in data:
        grams = data['grams']

    with get_session() as session:
        prod = session.query(Product).filter(Product.id == product_id).first()
        if not prod:
            abort(404)
        prod.name = name
        prod.calories = calories
        prod.proteins = proteins
        prod.fats = fats
        prod.carbs = carbs
        if grams is not None:
            prod.grams = grams
        session.commit()

    return {
        'result': True
    }


@BP.post('/<int:product_id>/archive')
@api_login_required_group(AccessGroup.Administrator)
def archive(product_id: int):
    with get_session() as session:
        prod = session.query(Product).filter(Product.id == product_id).first()
        if not prod:
            abort(404)

        prod.archived = True
        session.commit()

    return {
        'result': True
    }
