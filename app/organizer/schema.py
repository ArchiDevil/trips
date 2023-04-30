import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Float, Date, \
                       DateTime, Boolean, Enum as AlchemyEnum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


BASE = declarative_base()

class Units(PyEnum):
    '''Units used for products weight'''
    GRAMMS = 0
    PIECES = 1


class AccessGroup(PyEnum):
    '''Levels of privileges'''
    User = 0
    Administrator = 1


class UserType(PyEnum):
    '''Type of user'''
    Native = 0
    Vk = 1


class User(BASE):
    '''Describes a native user'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    # is nullable due to ability to use OAuth instead of raw password
    password = Column(String)
    displayed_name = Column(String)
    access_group = Column(AlchemyEnum(AccessGroup), nullable=False)
    user_type = Column(AlchemyEnum(UserType),
                       nullable=False, default=UserType.Native)
    last_logged_in = Column(DateTime, default=datetime.datetime.utcnow)

    trips = relationship('Trip', back_populates='user')
    shared_trips = relationship('Trip', secondary='tripaccess')


class Trip(BASE):
    '''Describes a trip'''
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    from_date = Column(Date, nullable=False)
    till_date = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey(User.__tablename__ + '.id'),
                        nullable=False)
    last_update = Column(DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    archived = Column(Boolean, default=False, nullable=False)

    user = relationship('User', back_populates='trips')
    groups = relationship('Group')


class Group(BASE):
    '''Describes a separate group in a trip'''
    __tablename__ = 'groups'

    trip_id = Column(Integer, ForeignKey(Trip.__tablename__ + '.id'),
                     primary_key=True)
    group_number = Column(Integer, primary_key=True)
    persons = Column(Integer, nullable=False)

    trip = relationship('Trip', back_populates='groups')


class Product(BASE):
    '''Describes a product'''
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
    '''Describes a meal record in a specific trip on a specific day'''
    __tablename__ = 'meal_records'

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey(Trip.__tablename__ + '.id'),
                     nullable=False)
    product_id = Column(Integer, ForeignKey(Product.__tablename__ + '.id'),
                        nullable=False)
    day_number = Column(Integer, nullable=False)
    meal_number = Column(Integer, nullable=False)
    mass = Column(Integer, nullable=False)


class VkUser(BASE):
    '''Describes a Vk registered user'''
    __tablename__ = 'vkusers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.__tablename__ + '.id'),
                     primary_key=True)
    user_token = Column(String, nullable=False)
    token_exp_time = Column(DateTime, nullable=False)
    photo_url = Column(String)


class TripAccess(BASE):
    '''Describes what users can access what trips'''
    __tablename__ = 'tripaccess'

    user_id = Column(Integer, ForeignKey(User.__tablename__ + '.id'),
                     primary_key=True)
    trip_id = Column(Integer, ForeignKey(Trip.__tablename__ + '.id'),
                     primary_key=True)


class SharingLink(BASE):
    '''Describes a link the user shared'''
    __tablename__ = 'sharinglinks'

    @staticmethod
    def make_expiration_date():
        return datetime.datetime.utcnow() + datetime.timedelta(days=3)

    uuid = Column(String, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.__tablename__ + '.id'))
    trip_id = Column(Integer, ForeignKey(Trip.__tablename__ + '.id'))
    expiration_date = Column(DateTime, nullable=False, default=make_expiration_date)


class PasswordLink(BASE):
    '''Describes a record to restore a password'''
    __tablename__ = 'passwordlinks'

    @staticmethod
    def make_expiration_date():
        return datetime.datetime.utcnow() + datetime.timedelta(days=3)

    uuid = Column(String, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.__tablename__ + '.id'))
    expiration_date = Column(DateTime, nullable=False, default=make_expiration_date)


def init_schema(engine):
    BASE.metadata.create_all(engine)
