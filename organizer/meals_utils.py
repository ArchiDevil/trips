from typing import List, Iterable, Any, Dict, Union, NamedTuple
import datetime


class MealRecord(NamedTuple):
    id: int
    day_number: int
    meal_number: int
    name: str
    mass: float
    proteins: float
    fats: float
    carbs: float
    calories: float


def calculate_day_info(day_number: int,
                       date: str,
                       meals_info: Iterable[MealRecord]
                       ) -> Dict[str, Union[int, str, List[Dict[str, Any]], Dict[str, int]]]:
    day = {
        'number': day_number,
        'date': date,

        'breakfast': [],
        'lunch': [],
        'dinner': [],
        'snacks': [],

        'breakfast_total': {'mass': 0},
        'lunch_total': {'mass': 0},
        'dinner_total': {'mass': 0},
        'snacks_total': {'mass': 0},

        'total_total': {'mass': 0}
    }

    meals_map = {
        0: 'breakfast',
        1: 'lunch',
        2: 'dinner',
        3: 'snacks'
    }

    for record in meals_info:
        meal_number: int = record.meal_number
        day[meals_map[meal_number]].append({
            'id': record.id,
            'name': record.name,
            'mass': record.mass,
            'proteins': record.proteins * record.mass / 100.0,
            'fats': record.fats * record.mass / 100.0,
            'carbs': record.carbs * record.mass / 100.0,
            'cals': record.calories * record.mass / 100.0
        })

    # calculating totals for each day
    for f in ('mass', 'proteins', 'fats', 'carbs', 'cals'):
        day['breakfast_total'][f] = sum([e[f] for e in day['breakfast']])
        day['lunch_total'][f] = sum([e[f] for e in day['lunch']])
        day['dinner_total'][f] = sum([e[f] for e in day['dinner']])
        day['snacks_total'][f] = sum([e[f] for e in day['snacks']])

        day['total_total'][f] = sum([day['breakfast_total'][f],
                                         day['lunch_total'][f],
                                         day['dinner_total'][f],
                                         day['snacks_total'][f]])

    return day


def format_date(first_day: datetime.date, current_day_number: int):
    return (first_day + datetime.timedelta(days=current_day_number - 1)).strftime('%d/%m')


def calculate_total_days_info(first_date: datetime.date,
                              last_date: datetime.date,
                              meals_info: Iterable[MealRecord]) -> List[Dict[str, Any]]:
    days_amount = (last_date - first_date).days + 1
    days = []

    for i in range(days_amount):
        date = format_date(first_date, i + 1)
        day_meals = [x for x in meals_info if x.day_number == i + 1]
        days.append(calculate_day_info(i + 1, date, day_meals))

    return days
