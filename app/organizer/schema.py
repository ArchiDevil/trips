import datetime
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column


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

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False)
    # is nullable due to ability to use OAuth instead of raw password
    password: Mapped[str] = mapped_column(nullable=True)
    displayed_name: Mapped[str] = mapped_column(nullable=True)
    access_group: Mapped[AccessGroup] = mapped_column(nullable=False)
    user_type: Mapped[UserType] = mapped_column(nullable=False, default=UserType.Native)
    last_logged_in: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow, nullable=True)

    trips: Mapped[list['Trip']] = relationship(back_populates='user')
    shared_trips: Mapped[list['Trip']] = relationship(secondary='tripaccess')


class Trip(BASE):
    '''Describes a trip'''
    __tablename__ = 'trips'

    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    from_date: Mapped[datetime.date] = mapped_column(nullable=False)
    till_date: Mapped[datetime.date] = mapped_column(nullable=False)
    created_by: Mapped[int] = mapped_column(
        ForeignKey(User.__tablename__ + '.id'), nullable=False
    )
    last_update: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.utcnow
    )
    archived: Mapped[bool] = mapped_column(default=False, nullable=False)

    user: Mapped['User'] = relationship(back_populates='trips')
    groups: Mapped[list['Group']] = relationship()


class Group(BASE):
    '''Describes a separate group in a trip'''
    __tablename__ = 'groups'

    trip_id: Mapped[int] = mapped_column(ForeignKey(Trip.__tablename__ + '.id'),
                                         primary_key=True)
    group_number: Mapped[int] = mapped_column(primary_key=True)
    persons: Mapped[int] = mapped_column(nullable=False)

    trip: Mapped['Trip'] = relationship(back_populates='groups')


class Product(BASE):
    '''Describes a product'''
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    calories: Mapped[float] = mapped_column(nullable=False)
    proteins: Mapped[float] = mapped_column(nullable=False)
    fats: Mapped[float] = mapped_column(nullable=False)
    carbs: Mapped[float] = mapped_column(nullable=False)
    grams: Mapped[float] = mapped_column(nullable=True)
    archived: Mapped[bool] = mapped_column(default=False, nullable=False)


class MealRecord(BASE):
    '''Describes a meal record in a specific trip on a specific day'''
    __tablename__ = 'meal_records'

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(
        ForeignKey(Trip.__tablename__ + '.id'), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(Product.__tablename__ + '.id'), nullable=False
    )
    day_number: Mapped[int] = mapped_column(nullable=False)
    meal_number: Mapped[int] = mapped_column(nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)


class VkUser(BASE):
    '''Describes a Vk registered user'''
    __tablename__ = 'vkusers'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.__tablename__ + '.id'), primary_key=True
    )
    user_token: Mapped[str] = mapped_column(nullable=False)
    token_exp_time: Mapped[datetime.datetime] = mapped_column(nullable=False)
    photo_url: Mapped[str] = mapped_column(nullable=True)


class TripAccess(BASE):
    '''Describes what users can access what trips'''
    __tablename__ = 'tripaccess'

    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.__tablename__ + '.id'), primary_key=True
    )
    trip_id: Mapped[int] = mapped_column(
        ForeignKey(Trip.__tablename__ + '.id'), primary_key=True
    )


def make_expiration_date():
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3)


class SharingLink(BASE):
    '''Describes a link the user shared'''
    __tablename__ = 'sharinglinks'

    uuid: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.__tablename__ + '.id'))
    trip_id: Mapped[int] = mapped_column(ForeignKey(Trip.__tablename__ + '.id'))
    expiration_date: Mapped[datetime.datetime] = mapped_column(nullable=False, default=make_expiration_date)


class PasswordLink(BASE):
    '''Describes a record to restore a password'''
    __tablename__ = 'passwordlinks'

    uuid: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.__tablename__ + '.id'))
    expiration_date: Mapped[datetime.datetime] = mapped_column(nullable=False, default=make_expiration_date)


def init_schema(engine):
    BASE.metadata.create_all(engine)
