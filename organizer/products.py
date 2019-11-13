from flask import Blueprint, render_template, request
import flask

from organizer.db import get_session
from organizer.schema import Product

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
def index():
    with get_session() as session:
        products = session.query(Product).filter(Product.archived == 0)
        return render_template('products/products.html', products=products, filtered=False)


@bp.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        calories = request.form['calories']
        proteins = request.form['proteins']
        fats = request.form['fats']
        carbs = request.form['carbs']

        grams = None
        if 'grams' in request.form.keys():
            grams = request.form['grams']

        with get_session() as session:
            prod = Product(name=name, calories=calories, proteins=proteins, fats=fats, carbs=carbs, grams=grams)
            session.add(prod)
            session.commit()

        return flask.redirect(flask.url_for('products.index'))

    return flask.redirect(flask.url_for('products.index'))


@bp.route('/archive/<int:product_id>')
def archive(product_id):
    with get_session() as session:
        prod = session.query(Product).filter(Product.id == product_id).one()
        prod.archived = 1
        session.commit()
    return flask.redirect(flask.url_for('products.index'))


@bp.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_request = request.form['request']
        search_request = "%{}%".format(search_request)

        with get_session() as session:
            found_products = session.query(Product).filter(
                Product.name.like(search_request), Product.archived != 1).all()
        return render_template('products/products.html', products=found_products, filtered=True)

    return flask.redirect(flask.url_for('products.index'))


@bp.route('/edit/<int:product_id>', methods=['POST'])
def edit(product_id):
    name = request.form['name']
    calories = request.form['calories']
    proteins = request.form['proteins']
    fats = request.form['fats']
    carbs = request.form['carbs']

    if 'grams' in request.form.keys():
        grams = request.form['grams']
    else:
        grams = None

    with get_session() as session:
        prod = session.query(Product).filter(Product.id == product_id).one()
        prod.name = name
        prod.calories = calories
        prod.proteins = proteins
        prod.fats = fats
        prod.carbs = carbs
        prod.grams = grams
        session.commit()

    return flask.redirect(flask.url_for('products.index'))
