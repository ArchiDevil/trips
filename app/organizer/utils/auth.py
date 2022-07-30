import requests
from flask import current_app
from sqlalchemy import or_

from organizer.schema import Trip, TripAccess, TripAccessType


def is_captcha_enabled() -> bool:
    return 'RECAPTCHA_SERVER_KEY' in current_app.config and current_app.config['RECAPTCHA_SERVER_KEY']


def check_captcha(response: str) -> bool:
    url = 'https://www.google.com/recaptcha/api/siteverify'
    answer = requests.post(url, data={
        'secret': current_app.config['RECAPTCHA_SERVER_KEY'],
        'response': response
    })

    if answer.status_code != 200:
        raise ConnectionError('Error from google server')

    return answer.json()['success']


def user_has_trip_access(trip: Trip, user_id: int, admin, session, access_type: TripAccessType):
    if trip.created_by == user_id or admin:
        return True

    if access_type == TripAccessType.Read:
        trip_access = session.query(TripAccess).filter(TripAccess.trip_id == trip.id,
                                                       TripAccess.user_id == user_id,
                                                       or_(TripAccess.access_type == TripAccessType.Read,
                                                           TripAccess.access_type == TripAccessType.Write)).first()
    else:
        trip_access = session.query(TripAccess).filter(TripAccess.trip_id == trip.id,
                                                       TripAccess.user_id == user_id,
                                                       TripAccess.access_type == TripAccessType.Write).first()

    return trip_access is not None
