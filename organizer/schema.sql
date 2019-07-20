DROP TABLE IF EXISTS trips;

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    from_date DATE,
    till_date DATE
);

--- fake data

INSERT INTO trips VALUES (
    1,
    "Test name",
    "2019-01-01",
    "2019-01-09"
);

INSERT INTO trips VALUES (
    2,
    "Another name, you know",
    "2019-06-01",
    "2019-07-09"
);

INSERT INTO trips VALUES (
    3,
    "Another name, you know",
    "2019-06-01",
    "2019-07-09"
);

INSERT INTO trips VALUES (
    4,
    "Another name, you know",
    "2019-06-01",
    "2019-07-09"
);

INSERT INTO trips VALUES (
    5,
    "Another name, you know",
    "2019-06-01",
    "2019-07-09"
);

INSERT INTO trips VALUES (
    6,
    "Another name, you know",
    "2019-06-01",
    "2019-07-09"
);

INSERT INTO trips VALUES (
    7,
    "Another name, you know",
    "2019-06-01",
    "2019-07-09"
);

INSERT INTO trips VALUES (
    8,
    "Another name, you know",
    "2019-06-01",
    "2019-07-09"
);

