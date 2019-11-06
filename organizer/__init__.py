import os

from flask import Flask, current_app


def before_first_request_handler():
    from . import db
    db_instance = db.get_db()
    result = db_instance.execute('SELECT * FROM sqlite_master').fetchone()
    if result is None:
        db.init_db()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import trips
    app.register_blueprint(trips.bp)
    app.add_url_rule('/', endpoint='index')

    from . import products
    app.register_blueprint(products.bp)

    from . import api
    app.register_blueprint(api.products_bp)
    app.register_blueprint(api.meals_bp)

    app.before_first_request(before_first_request_handler)

    return app
