import datetime
import os

from flask import Flask, current_app


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if 'DATABASE_URL' in os.environ:  # pragma: no cover
        db_url = os.environ['DATABASE_URL']  # pragma: no cover
    else: 
        db_url = 'sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite')

    secret_key = os.environ['SECRET_KEY'] if 'SECRET_KEY' in os.environ else 'dev'
    session_lifetime = datetime.timedelta(days=14)
    server_name = None
    if not test_config:
        server_name = os.environ['SERVER_NAME'] if 'SERVER_NAME' in os.environ else 'localhost:5000'

    vk_client_id = os.environ['VK_CLIENT_ID'] if 'VK_CLIENT_ID' in os.environ else None
    vk_app_secret = os.environ['VK_APP_SECRET'] if 'VK_APP_SECRET' in os.environ else None

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE=db_url,
        PERMANENT_SESSION_LIFETIME=session_lifetime,
        SERVER_NAME=server_name,
        VK_CLIENT_ID=vk_client_id,
        VK_APP_SECRET=vk_app_secret
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

    from . import auth
    app.register_blueprint(auth.bp)

    from . import trips
    app.register_blueprint(trips.bp)
    app.add_url_rule('/', endpoint='index')

    from . import meals
    app.register_blueprint(meals.bp)

    from . import products
    app.register_blueprint(products.bp)

    from . import api
    app.register_blueprint(api.products_bp)
    app.register_blueprint(api.meals_bp)

    from . import reports
    app.register_blueprint(reports.bp)

    from . import users
    app.register_blueprint(users.bp)

    from . import developer
    app.register_blueprint(developer.bp)

    @app.context_processor
    def inject_props():
        from . import schema
        return dict(AccessGroup=schema.AccessGroup)

    return app
