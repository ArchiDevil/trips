from flask import Blueprint, render_template, request
import flask

from organizer.db import get_db

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT * FROM products'
    ).fetchall()

    return render_template('products/products.j2', products=products)

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        calories = request.form['calories']
        proteins = request.form['proteins']
        fats = request.form['fats']
        carbs = request.form['carbs']

        db = get_db()

        db.execute(
            'INSERT INTO products(name, calories, proteins, fats, carbs) VALUES (?, ?, ?, ?, ?)',
            (name, calories, proteins, fats, carbs)
        )
        db.commit()
        return flask.redirect(flask.url_for('products.index'))

    return flask.redirect(flask.url_for('products.index'))
