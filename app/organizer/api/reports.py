from collections import defaultdict
from typing import Any, Literal

from flask import Blueprint, abort
from sqlalchemy import select
from sqlalchemy.sql import func

from organizer.auth import api_login_required_group
from organizer.db import get_session
from organizer.schema import AccessGroup, Group, MealRecord, Product, Trip

BP = Blueprint("reports", __name__, url_prefix="/reports")


@BP.get("/shopping/<trip_uid>")
@api_login_required_group(AccessGroup.User)
def shopping(trip_uid: str):
    with get_session() as session:
        trip = session.execute(select(Trip).where(Trip.uid == trip_uid)).scalar()
        if not trip:
            return abort(404)

        days_count = (trip.till_date - trip.from_date).days + 1

        persons_count = session.execute(
            select(func.sum(Group.persons)).where(Group.trip_id == trip.id)
        ).scalar()

        meals = session.execute(
            select(MealRecord.mass, Product.id, Product.name, Product.grams)
            .join(Product)
            .where(MealRecord.trip_id == trip.id)
            .where(MealRecord.day_number <= days_count)
        ).all()

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


@BP.get("/packing/<trip_uid>")
@api_login_required_group(AccessGroup.User)
def packing(trip_uid: str):
    with get_session() as session:
        trip = session.execute(select(Trip).where(Trip.uid == trip_uid)).scalar()
        if not trip:
            abort(404)

        days_count = (trip.till_date - trip.from_date).days + 1

        meals = session.execute(
            select(
                MealRecord.day_number,
                MealRecord.meal_number,
                MealRecord.mass,
                Product.name,
                Product.grams,
            )
            .join(Product)
            .where(MealRecord.trip_id == trip.id)
            .where(MealRecord.day_number <= days_count)
            .order_by(MealRecord.day_number)
        ).all()

        person_groups = (
            session.execute(select(Group.persons).where(Group.trip_id == trip.id))
            .scalars()
            .fetchall()
        )

    products: dict[
        int,
        list[
            dict[
                Literal["name", "meal", "mass", "grams"],
                str | int | float | list[int],
            ]
        ],
    ] = defaultdict(list)
    for meal in meals:
        day: int = meal.day_number
        products[day].append(
            {
                "name": meal.name,
                "meal": meal.meal_number,
                "mass": [meal.mass * persons for persons in person_groups],
            }
        )

        if meal.grams is not None:
            products[day][-1]["grams"] = meal.grams

    for arr in products.values():
        arr.sort(key=lambda x: x["meal"])

    return {"products": products}
