DROP TABLE IF EXISTS trips;

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    from_date DATE NOT NULL,
    till_date DATE NOT NULL,
    attendees INTEGER NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    archived INTEGER NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    calories REAL NOT NULL,
    proteins REAL NOT NULL,
    fats REAL NOT NULL,
    carbs REAL NOT NULL,
    grams REAL DEFAULT NULL,
    archived INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    access_group INTEGER NOT NULL
);

DROP TABLE IF EXISTS meal_records;

CREATE TABLE meal_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    day_number INTEGER NOT NULL,
    meal_number INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    mass INTEGER NOT NULL,

    FOREIGN KEY(trip_id) REFERENCES trips(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
