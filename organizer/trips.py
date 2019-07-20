from flask import Blueprint, render_template
import flask

from organizer.db import get_db

bp = Blueprint('trips', __name__)

@bp.route('/')
def index():
    db = get_db()
    days = db.execute(
        'SELECT name, from_date, till_date FROM trips'
    ).fetchall()

    return render_template('trips.j2', trip_days=days)
