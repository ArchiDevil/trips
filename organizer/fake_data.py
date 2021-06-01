from datetime import datetime

from organizer.schema import Trip, Product, MealRecord, User, AccessGroup, Group


def init_fake_data_internal(session):
    # password 'qwerty'
    admin = User(login="Administrator",
                 password="pbkdf2:sha256:150000$y8RuRagx$371e6520ae64c1c4c367adb82b076b081068333511ef3f2c3ccab0107494d5f0",
                 access_group=AccessGroup.Administrator)
    session.add(admin)

    # password 'org'
    org = User(login="Organizer",
               password="pbkdf2:sha256:150000$3ngYsSXZ$4a693ab6cacc753ed1b18ce51757e6d9d85c25ed02c422ec66dae70b92ea11b2",
               access_group=AccessGroup.TripManager)
    session.add(org)

    # password 'user1'
    session.add(User(login="User",
                     password="pbkdf2:sha256:150000$LXwcrYlk$45da8f74b50caf71fa6933de95bff3d959618c8098b2f0d45967cba2623cede3",
                     access_group=AccessGroup.Guest))

    trip1 = Trip(name="Taganay trip",
                 from_date=datetime.strptime("2019-01-01", "%Y-%m-%d"),
                 till_date=datetime.strptime("2019-01-05", "%Y-%m-%d"))
    trip1.groups.append(Group(group_number=0, persons=2))
    trip1.groups.append(Group(group_number=1, persons=3))

    trip2 = Trip(name="Archived trip",
                 from_date=datetime.strptime("2019-06-06", "%Y-%m-%d"),
                 till_date=datetime.strptime("2019-06-08", "%Y-%m-%d"),
                 archived=True)
    trip2.groups.append(Group(group_number=0, persons=1))

    trip3 = Trip(name="Admin trip",
                 from_date=datetime.strptime("2019-06-06", "%Y-%m-%d"),
                 till_date=datetime.strptime("2019-06-08", "%Y-%m-%d"))
    trip3.groups.append(Group(group_number=1, persons=1))

    org.trips.append(trip1)
    org.trips.append(trip2)
    admin.trips.append(trip3)

    session.commit()

    session.add(Product(name="Multigrain cereal", calories=362, proteins=11, fats=2, carbs=75))
    session.add(Product(name="Mango", calories=64, proteins=1, fats=1, carbs=78))
    session.add(Product(name="Cream cheese", calories=303, proteins=10, fats=27, carbs=5))
    session.add(Product(name="Belvita", calories=450, proteins=8.3, fats=16, carbs=65))
    session.add(Product(name="Borsch concentrate", calories=183.7, proteins=4, fats=5.5, carbs=17))
    session.add(Product(name="Beef jerk", calories=53.8, proteins=10.9, fats=1.12, carbs=0))
    session.add(Product(name="Crackers", calories=180.3, proteins=1.82, fats=14.4, carbs=11.8))
    session.add(Product(name="Chicken pate", calories=318, proteins=9, fats=30, carbs=3))
    session.add(Product(name="Ptitsa divnaya sweet", calories=439, proteins=2.6, fats=23.7, carbs=56, grams=5.5))
    session.add(Product(name="Lentils", calories=314, proteins=21.6, fats=1.1, carbs=48))
    session.add(Product(name="Chicken jerk", calories=244.5, proteins=52.3, fats=4.3, carbs=0))
    session.add(Product(name="Sausage", calories=472.7, proteins=24.8, fats=41.5, carbs=0))
    session.add(Product(name="Chocolate", calories=550, proteins=6.9, fats=35.7, carbs=54.4))
    session.add(Product(name="Step snack", calories=455.9, proteins=9.6, fats=26.1, carbs=47.3, grams=12.0))
    session.add(Product(name="Archived thingy :)", calories=51, proteins=2, fats=3, carbs=3, archived=True))

    session.commit()

    for x in range(4, -1, -1):
        if x == 3:
            continue

        if x == 0:
            session.add_all([
                MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=1, mass=60),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=2, mass=20),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=3, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=4, mass=50),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=5, mass=50),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=6, mass=20),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=7, mass=15),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=8, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=9, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=10, mass=60),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=11, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=12, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=13, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=3, product_id=14, mass=60)
            ])
        else:
            session.add_all([
                MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=1, mass=60),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=4, mass=50),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=5, mass=50),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=8, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=9, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=10, mass=60),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=13, mass=30),
                MealRecord(trip_id=1, day_number=x + 1, meal_number=3, product_id=14, mass=60)
            ])
    session.commit()
