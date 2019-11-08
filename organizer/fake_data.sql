DELETE FROM trips;
INSERT INTO trips(name, from_date, till_date, attendees) VALUES ("Taganay trip", "2019-01-01", "2019-01-09", 3);

---

DELETE FROM products;
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Multigrain cereal", 360, 11,  2, 75);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Mango", 64, 1, 1, 78);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Cream cheese", 303, 10, 27, 5);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Belvita", 450, 8.3, 16, 65);

INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Borsch concentrate", 183.7, 4, 5.5, 17);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Beef jerk", 53.8, 10.9, 1.12, 0);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Crackers", 180.3, 1.82, 14.4, 11.8);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Chicken pate", 318, 9, 30, 3);
INSERT INTO products(name, calories, proteins, fats, carbs, grams) VALUES ("Ptitsa divnaya sweet", 439, 2.6, 23.7, 56, 5.5);

INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Lentils", 314, 21.6, 1.1, 48);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Chicken jerk", 244.5, 52.3, 4.3, 0);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Sausage", 472.7, 24.8, 41.5, 0);
INSERT INTO products(name, calories, proteins, fats, carbs) VALUES ("Chocolate", 550, 6.9, 35.7, 54.4);

INSERT INTO products(name, calories, proteins, fats, carbs, grams) VALUES ("Step snack", 455.9, 9.6, 26.1, 47.3, 12.0);

---

INSERT INTO products(name, calories, proteins, fats, carbs, archived) VALUES (
    "Archived thingy :)",
    51,
    2, 3, 3, 
    1
);

---

DELETE FROM meal_records;
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 0,  1, 60);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 0,  2, 20);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 0,  3, 30);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 0,  4, 50);

INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 1,  5, 50);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 1,  6, 20);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 1,  7, 15);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 1,  8, 30);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 1,  9, 30);

INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 2, 10, 60);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 2, 11, 30);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 2, 12, 30);
INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 2, 13, 30);

INSERT INTO meal_records(trip_id, day_number, meal_number, product_id, mass) VALUES (1, 1, 3, 14, 60);

---

DELETE FROM users;
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
