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
    archived INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    access_group INTEGER NOT NULL
);

--- fake data

INSERT INTO trips(name, from_date, till_date, attendees) VALUES (
    "Mt. Everest trip",
    "2019-01-01",
    "2019-01-09",
    5
);

INSERT INTO trips(name, from_date, till_date, attendees) VALUES (
    "Rocky Mountains",
    "2019-06-01",
    "2019-07-09",
    3
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

INSERT INTO products(name, calories, proteins, fats, carbs, archived) VALUES (
    "Archived thingy :)",
    51,
    2, 3, 3, 
    1
);

---

--- password 'qwerty'
INSERT INTO users(name, password, access_group)
VALUES ("Administrator", "pbkdf2:sha256:150000$y8RuRagx$371e6520ae64c1c4c367adb82b076b081068333511ef3f2c3ccab0107494d5f0", 0);

--- password 'org'
INSERT INTO users(name, password, access_group)
VALUES ("Organizer",     "pbkdf2:sha256:150000$3ngYsSXZ$4a693ab6cacc753ed1b18ce51757e6d9d85c25ed02c422ec66dae70b92ea11b2", 1);

--- password 'user1'
INSERT INTO users(name, password, access_group)
VALUES ("User1",         "pbkdf2:sha256:150000$LXwcrYlk$45da8f74b50caf71fa6933de95bff3d959618c8098b2f0d45967cba2623cede3", 2);

--- password 'user2'
INSERT INTO users(name, password, access_group)
VALUES ("User2",         "pbkdf2:sha256:150000$eR8YdWL9$1edf7f04de6f688c179a276dfac1416d0faf5ae583ab608617d8317846532f2b", 2);
