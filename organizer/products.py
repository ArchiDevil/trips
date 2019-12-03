import math

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Product, AccessGroup

bp = Blueprint('products', __name__, url_prefix='/products')


class RedirectError(RuntimeError):
    def __init__(self, url):
        super().__init__()
        self.__url = url

    @property
    def url(self):
        return self.__url


def check_input_data():
    name = str(request.form['name'])
    if not name:
        flash('Incorrect name')
        raise RedirectError(url_for('products.index'))

    try:
        calories = float(request.form['calories'])
        if calories < 0 or math.isnan(calories):
            raise ValueError
    except ValueError:
        flash('Incorrect calories')
        raise RedirectError(url_for('products.index'))

    try:
        proteins = float(request.form['proteins'])
        if not (proteins >= 0 and proteins <= 100):
            raise ValueError
    except ValueError:
        flash('Incorrect proteins')
        raise RedirectError(url_for('products.index'))

    try:
        fats = float(request.form['fats'])
        if not (fats >= 0 and fats <= 100):
            raise ValueError
    except ValueError:
        flash('Incorrect fats')
        raise RedirectError(url_for('products.index'))

    try:
        carbs = float(request.form['carbs'])
        if not (carbs >= 0 and carbs <= 100):
            raise ValueError
    except ValueError:
        flash('Incorrect carbohydrates')
        raise RedirectError(url_for('products.index'))

    grams = None
    if 'grams' in request.form.keys():
        try:
            grams = float(request.form['grams'])
            if grams < 0 or math.isnan(grams):
                raise ValueError
        except ValueError:
            flash('Incorrect grams per piece')
            raise RedirectError(url_for('products.index'))


@bp.route('/')
@login_required_group(AccessGroup.Guest)
def index():
    with get_session() as session:
        page = 0
        products_per_page = 10
        if 'page' in request.args:
            page = int(request.args['page'])

        search = None
        if 'search' in request.args:
            search = request.args['search']

        if search:
            search_pattern = "%{}%".format(search)
            products_count = session.query(Product.id).filter(Product.name.ilike(search_pattern),
                                                              Product.archived == False).count()
            products = session.query(Product).filter(Product.name.ilike(search_pattern),
                                                     Product.archived == False).offset(page * products_per_page).limit(products_per_page).all()
        else:
            products_count = session.query(Product.id).filter(Product.archived == False).count()
            products = session.query(Product).filter(Product.archived == False).offset(page * products_per_page).limit(products_per_page).all()
        return render_template('products/products.html', products=products,
                               search=search, page=page,
                               last_page=math.ceil(products_count / products_per_page) - 1)


@bp.route('/add', methods=['POST'])
@login_required_group(AccessGroup.TripManager)
def add():
    try:
        check_input_data()
    except RedirectError as exc:
        return redirect(exc.url)
    
    name = request.form['name']
    calories = request.form['calories']
    proteins = request.form['proteins']
    fats = request.form['fats']
    carbs = request.form['carbs']

    grams = None
    if 'grams' in request.form.keys():
        grams = request.form['grams']

    with get_session() as session:
        prod = Product(name=name, calories=calories,
                       proteins=proteins, fats=fats,
                       carbs=carbs, grams=grams)
        session.add(prod)
        session.commit()

    return redirect(url_for('products.index'))


@bp.route('/archive/<int:product_id>')
@login_required_group(AccessGroup.TripManager)
def archive(product_id):
    with get_session() as session:
        prod = session.query(Product).filter(Product.id == product_id).first()
        if not prod:
            abort(404)
        prod.archived = True
        session.commit()
        return redirect(url_for('products.index'))


@bp.route('/edit/<int:product_id>', methods=['POST'])
@login_required_group(AccessGroup.TripManager)
def edit(product_id):
    try:
        check_input_data()
    except RedirectError as exc:
        return redirect(exc.url)

    name = request.form['name']
    calories = request.form['calories']
    proteins = request.form['proteins']
    fats = request.form['fats']
    carbs = request.form['carbs']

    grams = None
    if 'grams' in request.form.keys():
        grams = request.form['grams']

    with get_session() as session:
        prod = session.query(Product).filter(Product.id == product_id).first()
        if not prod:
            abort(404)
        prod.name = name
        prod.calories = calories
        prod.proteins = proteins
        prod.fats = fats
        prod.carbs = carbs
        prod.grams = grams
        session.commit()

    return redirect(url_for('products.index'))
