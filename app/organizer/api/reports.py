from typing import Any, Optional
from flask import Blueprint, abort
from sqlalchemy.sql import func

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import AccessGroup, Group, MealRecord, Product, Trip

BP = Blueprint("reports", __name__, url_prefix="/reports")


@BP.get("/shopping/<trip_uid>")
@api_login_required_group(AccessGroup.User)
def shopping(trip_uid: str):
    with get_session() as session:
        trip: Optional[Trip] = session.query(Trip).filter(Trip.uid == trip_uid).first()
        if not trip:
            return abort(404)

        persons_count = (
            session.query(func.sum(Group.persons))
            .filter(Group.trip_id == trip.id)
            .scalar()
        )
        meals = (
            session.query(MealRecord.mass, Product.id, Product.name, Product.grams)
            .join(Product)
            .filter(MealRecord.trip_id == trip.id)
            .all()
        )

    products: dict[int, dict[str, Any]] = {}
    for meal in meals:
        if meal.id not in products:
            products[meal.id] = {"id": meal.id, "name": meal.name, "mass": 0}
            if meal.grams is not None:
                products[meal.id]["pieces"] = 0

        products[meal.id]["mass"] += meal.mass * persons_count
        if meal.grams is not None:
            products[meal.id]["pieces"] += meal.mass * persons_count / meal.grams

    return list(products.values())
