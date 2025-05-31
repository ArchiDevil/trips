import requests
from flask import current_app
from sqlalchemy.orm import Session

from organizer.schema import Trip, TripAccess


def is_captcha_enabled() -> bool:
    return 'RECAPTCHA_SERVER_KEY' in current_app.config and current_app.config['RECAPTCHA_SERVER_KEY']


def check_captcha(response: str) -> bool:
    url = 'https://www.google.com/recaptcha/api/siteverify'
    answer = requests.post(url, data={
        'secret': current_app.config['RECAPTCHA_SERVER_KEY'],
        'response': response
    }, timeout=10.0)

    if answer.status_code != 200:
        raise ConnectionError('Error from google server')

    return answer.json()['success']


def user_has_trip_access(trip: Trip, user_id: int, admin: bool, session: Session) -> bool:
    if trip.created_by == user_id or admin:
        return True

    trip_access = session.query(TripAccess).filter(TripAccess.trip_id == trip.id,
                                                   TripAccess.user_id == user_id).first()

    return trip_access is not None
