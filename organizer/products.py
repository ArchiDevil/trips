import math

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from sentry_sdk import capture_exception

from organizer.auth import login_required_group
from organizer.db import get_session
from organizer.schema import Product, AccessGroup
from organizer.strings import STRING_TABLE

bp = Blueprint('products', __name__, url_prefix='/products')


def check_input_data():
    name = str(request.form['name'])
    if not name:
        raise RuntimeError(STRING_TABLE['Products error incorrect name'])

    try:
        calories = float(request.form['calories'])
        if calories < 0 or math.isnan(calories):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect calories'])

    try:
        proteins = float(request.form['proteins'])
        if not (proteins >= 0 and proteins <= 100):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect proteins'])

    try:
        fats = float(request.form['fats'])
        if not (fats >= 0 and fats <= 100):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect fats'])

    try:
        carbs = float(request.form['carbs'])
        if not (carbs >= 0 and carbs <= 100):
            raise ValueError
    except ValueError:
        raise RuntimeError(STRING_TABLE['Products error incorrect carbs'])

    grams = None
    if 'grams' in request.form.keys():
        try:
            grams = float(request.form['grams'])
            if grams < 0 or math.isnan(grams):
                raise ValueError
        except ValueError:
            raise RuntimeError(STRING_TABLE['Products error incorrect grams'])


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
            products = session.query(Product).filter(Product.name.ilike(search_pattern), Product.archived == False).order_by(
                Product.id).offset(page * products_per_page).limit(products_per_page).all()
        else:
            products_count = session.query(Product.id).filter(Product.archived == False).count()
            products = session.query(Product).filter(Product.archived == False).order_by(
                Product.id).offset(page * products_per_page).limit(products_per_page).all()
        return render_template('products/products.html', products=products,
                               search=search, page=page,
                               last_page=math.ceil(products_count / products_per_page) - 1)


@bp.route('/add', methods=['POST'])
@login_required_group(AccessGroup.TripManager)
def add():
    redirect_location = request.referrer if request.referrer else request.headers.get('Referer')
    if not redirect_location:
        redirect_location = url_for('.index')
    try:
        check_input_data()
    except RuntimeError as exc:
        capture_exception(exc)
        flash(str(exc))
        return redirect(redirect_location)

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

    return redirect(redirect_location)


@bp.route('/archive/<int:product_id>')
@login_required_group(AccessGroup.TripManager)
def archive(product_id):
    redirect_location = request.referrer if request.referrer else request.headers.get('Referer')
    if not redirect_location:
        redirect_location = url_for('.index')
    with get_session() as session:
        prod = session.query(Product).filter(Product.id == product_id).first()
        if not prod:
            abort(404)
        prod.archived = True
        session.commit()
        return redirect(redirect_location)


@bp.route('/edit/<int:product_id>', methods=['POST'])
@login_required_group(AccessGroup.TripManager)
def edit(product_id):
    redirect_location = request.referrer if request.referrer else request.headers.get('Referer')
    if not redirect_location:
        redirect_location = url_for('.index')
    try:
        check_input_data()
    except RuntimeError as exc:
        capture_exception(exc)
        flash(str(exc))
        return redirect(redirect_location)

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

    return redirect(redirect_location)
