import datetime
import os

from flask import Flask

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from werkzeug.middleware.proxy_fix import ProxyFix

if 'SENTRY_DSN' in os.environ:  # pragma: no cover
    sentry_sdk.init(os.environ['SENTRY_DSN'],  # pragma: no cover
                    integrations=[FlaskIntegration(), SqlalchemyIntegration()])  # pragma: no cover


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1
    )

    db_url = os.environ.get('DATABASE_URL',
                            'sqlite:///' + os.path.join(app.instance_path,
                                                        'flaskr.sqlite'))

    if db_url.startswith('postgres://'): # for Heroku deployment
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    secret_key = os.environ.get('SECRET_KEY', 'dev')
    session_lifetime = datetime.timedelta(days=14)
    server_name = None
    if not test_config:
        server_name = os.environ.get('SERVER_NAME', 'localhost:5000')

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE=db_url,
        PERMANENT_SESSION_LIFETIME=session_lifetime,
        SERVER_NAME=server_name,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    vk_client_id = os.environ.get('VK_CLIENT_ID', None)
    vk_app_secret = os.environ.get('VK_APP_SECRET', None)
    if vk_client_id and vk_app_secret:
        app.config.from_mapping(
            VK_CLIENT_ID=vk_client_id,
            VK_APP_SECRET=vk_app_secret,
        )

    recaptcha_server_key = os.environ.get('RECAPTCHA_SERVER_KEY', None)
    if recaptcha_server_key:
        app.config.from_mapping(
            RECAPTCHA_SERVER_KEY=recaptcha_server_key
        )

    sendinblue_api_key = os.environ.get('SENDINBLUE_API_KEY', None)
    if sendinblue_api_key:
        app.config.from_mapping(
            SENDINBLUE_API_KEY=sendinblue_api_key
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

    from . import api
    app.register_blueprint(api.BP)

    @app.context_processor
    def inject_props():
        from . import schema
        from . import strings
        return {
            'AccessGroup': schema.AccessGroup,
            'string_table': strings.STRING_TABLE,
            'today_date': datetime.datetime.today().strftime('%d-%m-%Y'),
            'environment': app.config.get('ENV', 'production'),
        }

    return app
