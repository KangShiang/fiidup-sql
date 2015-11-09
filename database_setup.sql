--#######################################################--
--# This is the sql script to setup the fiidup SQL      #--
--# database with all necessary tables and constraints  #--
--#######################################################--

-- ###### TABLES FOR USERS ###### --
CREATE TABLE IF NOT EXISTS person
(
user_id int NOT NULL AUTO_INCREMENT,
username varchar(255) NOT NULL UNIQUE,
password text NOT NULL,
email varchar(255) NOT NULL UNIQUE,
fiider_count int DEFAULT 0,
fiiding_count int DEFAULT 0,
post_count int DEFAULT 0,
profile_pic_url text UNIQUE,
background_pic_url text UNIQUE,
PRIMARY KEY (user_id)
);
--- add from fb:
-- facebookId BIGINT
-- first name
-- last name


CREATE TABLE IF NOT EXISTS follow
(
follower int NOT NULL,
following int NOT NULL,
PRIMARY KEY (follower, following),
FOREIGN KEY (follower) REFERENCES person(user_id) ON DELETE CASCADE,
FOREIGN KEY (following) REFERENCES person(user_id) ON DELETE CASCADE
);

-- ###### TABLES FOR DISHES ###### --
CREATE TABLE IF NOT EXISTS dish
(
dish_id int NOT NULL AUTO_INCREMENT,
dish_name text NOT NULL,
restaurant_id int NOT NULL,
user_id int NOT NULL,
url varchar(255) NOT NULL UNIQUE,
posted_time double NOT NULL,
caption text,
price int(1),
tags text,
location point,
like_count int DEFAULT 0,
comment_count int DEFAULT 0,
tasted_count int DEFAULT 0,
keep_count int DEFAULT 0,
PRIMARY KEY (dish_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id) ON DELETE CASCADE,
FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comment
(
comment_id int NOT NULL AUTO_INCREMENT,
dish_id int NOT NULL,
comment text NOT NULL,
user_id int NOT NULL,
posted_time double NOT NULL,
PRIMARY KEY (comment_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE,
FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_keep
(
dish_id int NOT NULL,
user_id int NOT NULL,
PRIMARY KEY (dish_id, user_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE,
FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_like
(
dish_id int NOT NULL,
user_id int NOT NULL,
PRIMARY KEY (dish_id, user_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE,
FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_tasted
(
dish_id int NOT NULL,
user_id int NOT NULL,
PRIMARY KEY (dish_id, user_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE,
FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

-- ###### TABLES FOR RESTAURANTS ###### --
CREATE TABLE IF NOT EXISTS restaurant
(
restaurant_id int NOT NULL AUTO_INCREMENT,
restaurant_name text NOT NULL UNIQUE,
tags text,
location point,
like_count int DEFAULT 0,
review_count int DEFAULT 0,
visited_count int DEFAULT 0,
keep_count int DEFAULT 0,
PRIMARY KEY (restaurant_id)
);
-- add
-- opening hours - object

CREATE TABLE IF NOT EXISTS review
(
review_id int NOT NULL AUTO_INCREMENT,
restaurant_id int NOT NULL,
user_id text NOT NULL,
review text NOT NULL,
PRIMARY KEY (review_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS restaurant_keep
(
restaurant_id int NOT NULL,
user_id text,
PRIMARY KEY (restaurant_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS restaurant_like
(
restaurant_id int NOT NULL,
user_id text,
PRIMARY KEY (restaurant_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS restaurant_visited
(
restaurant_id int NOT NULL,
user_id text,
PRIMARY KEY (restaurant_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id) ON DELETE CASCADE
);

-- ###### TRIGGERS ###### --
-- A trigger to insert the user_id into other tables associated with user
DROP TRIGGER IF EXISTS user_updater;
-- deprecated
DELIMITER |
CREATE TRIGGER user_updater
AFTER INSERT ON person FOR EACH ROW
BEGIN
INSERT INTO following(user_id) VALUES (NEW.user_id);
INSERT INTO follower(user_id) VALUES (NEW.user_id);
END |
DELIMITER ;

-- A trigger to insert the dish_id into other tables associated with dish
DROP TRIGGER IF EXISTS dish_updater;
-- deprecated
DELIMITER |
CREATE TRIGGER dish_updater
AFTER INSERT ON dish FOR EACH ROW
BEGIN
INSERT INTO dish_keep(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_like(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_tasted(dish_id) VALUES (NEW.dish_id);
END |
DELIMITER ;

-- A trigger to insert the restaurant_id into other tables associated with restaurant
DROP TRIGGER IF EXISTS restaurant_updater;

DELIMITER |
CREATE TRIGGER restaurant_updater
AFTER INSERT ON restaurant FOR EACH ROW
BEGIN
INSERT INTO restaurant_keep(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_like(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_visited(restaurant_id) VALUES (NEW.restaurant_id);
END |
DELIMITER ;


--- TEST SCRIPTS ---
DROP TRIGGER dish_updater;
DROP TABLE dish_tasted;
DROP TABLE dish_keep;
DROP TABLE dish_like;
DROP TABLE comment;
DROP TABLE dish;

INSERT INTO restaurant (restaurant_name) VALUES ('rest1');
INSERT INTO restaurant (restaurant_name) VALUES ('rest2');
INSERT INTO dish (dish_name, restaurant_id, user_id, url, posted_time) VALUES ('dish1', 1, 13, 'http://a', '123.12');

SELECT dish.*, person.username
FROM dish
INNER JOIN person
ON dish_id>1 AND dish.user_id=person.user_id;
