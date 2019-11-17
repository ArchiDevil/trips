import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, Enum as AlchemyEnum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


BASE = declarative_base()


class Trip(BASE):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    from_date = Column(Date, nullable=False)
    till_date = Column(Date, nullable=False)
    attendees = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    archived = Column(Boolean, default=False, nullable=False)
    users = relationship('User', secondary='tripaccess')


class Product(BASE):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    proteins = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    grams = Column(Float)
    archived = Column(Boolean, default=False, nullable=False)


class MealRecord(BASE):
    __tablename__ = 'meal_records'

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey(
        Trip.__tablename__ + '.id'), nullable=False)
    product_id = Column(Integer, ForeignKey(
        Product.__tablename__ + '.id'), nullable=False)
    day_number = Column(Integer, nullable=False)
    meal_number = Column(Integer, nullable=False)
    mass = Column(Integer, nullable=False)


class AccessGroup(PyEnum):
    Guest = 0
    TripManager = 1
    Administrator = 2


class User(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # is nullable due to ability to use OAuth instead of raw password
    password = Column(String)
    access_group = Column(AlchemyEnum(AccessGroup), nullable=False)
    trips = relationship('Trip', secondary='tripaccess')


class TripAccess(BASE):
    __tablename__ = 'tripaccess'

    user_id = Column(Integer, ForeignKey(User.__tablename__ + '.id'), primary_key=True)
    trip_id = Column(Integer, ForeignKey(Trip.__tablename__ + '.id'), primary_key=True)


def init_schema(engine):
    BASE.metadata.create_all(engine)
