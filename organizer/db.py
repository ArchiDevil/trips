from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import click
from flask import current_app, g
from flask.cli import with_appcontext

from organizer.schema import init_schema as init_schema_internal, BASE
from organizer.fake_data import init_fake_data_internal


@contextmanager
def get_session():
    # this is the first request to the DB
    if 'engine' not in g:
        init_connection()
    try:
        session = g.sessionmaker()
        yield session
    finally:
        g.sessionmaker.remove()


def init_connection():
    engine = create_engine(
        current_app.config['DATABASE']
    )
    g.engine = engine
    session_factory = sessionmaker(bind=engine)
    g.sessionmaker = scoped_session(session_factory)


def close_connection(e=None):
    g.pop('sessionmaker', None)
    engine = g.pop('engine', None)
    if engine is not None:
        engine.dispose()


def re_init_schema():
    BASE.metadata.drop_all(g.engine)
    init_schema_internal(g.engine)


def init_fake_data():
    with get_session() as session:
        init_fake_data_internal(session)


@click.command('init-empty-db')
@with_appcontext
def init_empty_db_command():
    """Clear the existing data and create new tables."""
    init_connection()
    re_init_schema()
    click.echo('Initialized the database')


@click.command('init-fake-data')
@with_appcontext
def init_fake_data_command():
    """Fill the tables with some fake data."""
    init_connection()
    re_init_schema()
    init_fake_data()
    click.echo('Tables filled with fake data')


def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_empty_db_command)
    app.cli.add_command(init_fake_data_command)
