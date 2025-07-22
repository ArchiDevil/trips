from flask import Blueprint, g, abort
from sqlalchemy import text, select, func

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import AccessGroup, Product, MealRecord, Trip

BP = Blueprint("maintenance", __name__, url_prefix="/maintenance")


@BP.post("/vacuum")
@api_login_required_group(AccessGroup.Administrator)
def vacuum():
    with g.engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        connection.execute(text("VACUUM (FULL, ANALYZE)"))

    return [], 200


@BP.post("/reindex/<table>")
@api_login_required_group(AccessGroup.Administrator)
def reindex(table: str):
    if table != "trips":
        # avoid other tables
        # we aware as provided argument is passed as a string DIRECTLY to the DB
        # if the check is removed here this might lead to SQL injection!
        abort(404)

    with get_session() as session:
        session.execute(text("ANALYZE"))
        session.execute(text(f"REINDEX TABLE {table}"))

    return [], 200


@BP.get("/unused-products")
@api_login_required_group(AccessGroup.Administrator)
def get_unused_products():
    with get_session() as session:
        count_func = func.count(MealRecord.id)
        products = session.execute(
            select(Product.id, Product.name, Product.archived, count_func)
            .join(MealRecord, isouter=True)
            .group_by(Product.id, Product.name, Product.archived)
            .having(count_func == 0)
            .order_by(Product.id)
        )
    return [
        {"id": product.id, "name": product.name, "archived": product.archived}
        for product in products.all()
    ]


@BP.get("/empty-trips")
@api_login_required_group(AccessGroup.Administrator)
def get_empty_trips():
    with get_session() as session:
        count_func = func.count(MealRecord.id)
        trips = session.execute(
            select(Trip.id, Trip.name, Trip.archived, Trip.uid, count_func)
            .join(MealRecord, isouter=True)
            .group_by(Trip.id)
            .having(count_func == 0)
            .order_by(Trip.id)
        )
    return [
        {"name": trip.name, "archived": trip.archived, "uid": trip.uid}
        for trip in trips.all()
    ]
