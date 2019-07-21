DROP TABLE IF EXISTS trips;

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    from_date DATE,
    till_date DATE
);

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    calories REAL,
    proteins REAL,
    fats REAL,
    carbs REAL
);

--- fake data

INSERT INTO trips(name, from_date, till_date) VALUES (
    "First card",
    "2019-01-01",
    "2019-01-09"
);

INSERT INTO trips(name, from_date, till_date) VALUES (
    "Second card",
    "2019-06-01",
    "2019-07-09"
);

---

INSERT INTO products(name, calories, proteins, fats, carbs) VALUES (
    "Some soup",
    431,
    2, 3, 45
);

INSERT INTO products(name, calories, proteins, fats, carbs) VALUES (
    "Some meat",
    221,
    22, 3, 3
);
