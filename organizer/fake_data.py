from datetime import datetime

from organizer.schema import Trip, Product, MealRecord

def init_fake_data_internal(session):
    session.add(Trip(name="Taganay trip",
                     from_date=datetime.strptime("2019-01-01", "%Y-%m-%d"),
                     till_date=datetime.strptime("2019-01-09", "%Y-%m-%d"),
                     attendees=3))

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
    session.add(Product(name="Archived thingy :)", calories=51, proteins=2, fats=3, carbs=3, archived=1))

    for x in range(10):
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=1, mass=60))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=2, mass=20))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=3, mass=30))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=0, product_id=4, mass=50))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=5, mass=50))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=6, mass=20))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=7, mass=15))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=8, mass=30))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=1, product_id=9, mass=30))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=10, mass=60))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=11, mass=30))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=12, mass=30))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=2, product_id=13, mass=30))
        session.add(MealRecord(trip_id=1, day_number=x + 1, meal_number=3, product_id=14, mass=60))

    session.commit()
