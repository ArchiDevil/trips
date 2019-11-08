from flask import Blueprint, render_template, request
import flask

from organizer.db import get_db

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT * FROM products WHERE archived=0'
    ).fetchall()
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

        db = get_db()

        db.execute(
            'INSERT INTO products(name, calories, proteins, fats, carbs, grams) VALUES (?, ?, ?, ?, ?, ?)',
            [name, calories, proteins, fats, carbs, grams]
        )
        db.commit()
        return flask.redirect(flask.url_for('products.index'))

    return flask.redirect(flask.url_for('products.index'))


@bp.route('/archive/<int:product_id>')
def archive(product_id):
    db = get_db()

    db.execute(
        'UPDATE products SET archived=1 WHERE id=?',
        [product_id]
    )
    db.commit()
    return flask.redirect(flask.url_for('products.index'))


@bp.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_request = request.form['request']
        search_request = "%{}%".format(search_request)

        db = get_db()
        found_products = db.execute(
            "SELECT * FROM products WHERE name LIKE ? AND NOT archived=1",
            [search_request]
        ).fetchall()

        return render_template('products/products.html', products=found_products, filtered=True)

    return flask.redirect(flask.url_for('products.index'))


@bp.route('/edit/<int:product_id>', methods=['POST'])
def edit(product_id):
    name = request.form['name']
    calories = request.form['calories']
    proteins = request.form['proteins']
    fats = request.form['fats']
    carbs = request.form['carbs']

    db = get_db()
    if 'grams' in request.form.keys():
        grams = request.form['grams']
    else:
        grams = None
    db.execute(
        'UPDATE products SET name=?, calories=?, proteins=?, fats=?, carbs=?, grams=? WHERE id=?',
        [name, calories, proteins, fats, carbs, grams, product_id]
    )
    db.commit()
    return flask.redirect(flask.url_for('products.index'))
