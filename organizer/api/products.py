from typing import Final

from flask import Blueprint, request, url_for

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import Product, Units, AccessGroup


BP = Blueprint('products', __name__, url_prefix='/products')


@BP.get('/search')
@api_login_required_group(AccessGroup.Guest)
def search():
    products_per_page: Final = 10
    page = int(request.args.get('page', 0))
    search_request = request.args.get('search', '')

    with get_session() as session:
        if search_request:
            search_pattern = f"%{search_request}%"
            products_count = session.query(Product.id).filter(Product.name.ilike(search_pattern),
                                                              Product.archived == False).count()
            products = session.query(Product).filter(Product.name.ilike(search_pattern),
                                                     Product.archived == False).order_by(Product.id).offset(page * products_per_page).limit(products_per_page).all()
        else:
            products_count = session.query(Product.id).filter(Product.archived == False).count()
            products = session.query(Product).filter(Product.archived == False).order_by(Product.id).offset(page * products_per_page).limit(products_per_page).all()

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
                    'edit_link': url_for('products.edit', product_id=product.id),
                    'archive_link': url_for('products.archive', product_id=product.id)
                } for product in products
            ]
        }


@BP.get('/units')
@api_login_required_group()
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
