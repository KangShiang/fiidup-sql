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
profile_pic_url text,
background_pic_url text,
PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS following
(
user_id int NOT NULL,
following text,
PRIMARY KEY (user_id),
FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS follower
(
user_id int NOT NULL,
follower text,
PRIMARY KEY (user_id),
FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

-- ###### TABLES FOR DISHES ###### --
CREATE TABLE IF NOT EXISTS dish
(
dish_id int NOT NULL AUTO_INCREMENT,
dish_name text NOT NULL,
restaurant_id text NOT NULL,
user_id text NOT NULL,
url text NOT NULL,
posted_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(),
caption text,
price double,
tags text,
location point,
like_count int DEFAULT 0,
comment_count int DEFAULT 0,
tasted_count int DEFAULT 0,
keep_count int DEFAULT 0,
PRIMARY KEY (dish_id)
);

CREATE TABLE IF NOT EXISTS comment
(
comment_id int NOT NULL AUTO_INCREMENT,
dish_id int NOT NULL,
comment text NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (comment_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_keep
(
dish_id int NOT NULL,
user_id text,
PRIMARY KEY (dish_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_like
(
dish_id int NOT NULL,
user_id text,
PRIMARY KEY (dish_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_tasted
(
dish_id int NOT NULL,
user_id text,
PRIMARY KEY (dish_id),
FOREIGN KEY (dish_id) REFERENCES dish(dish_id) ON DELETE CASCADE
);

-- ###### TABLES FOR RESTAURANTS ###### --
CREATE TABLE IF NOT EXISTS restaurant
(
restaurant_id int NOT NULL AUTO_INCREMENT,
restaurant_name text NOT NULL,
tags text,
location point,
like_count int DEFAULT 0,
review_count int DEFAULT 0,
visited_count int DEFAULT 0,
keep_count int DEFAULT 0,
PRIMARY KEY (restaurant_id)
);

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

DELIMITER |
CREATE TRIGGER user_updater
AFTER INSERT ON `person` FOR EACH ROW
BEGIN
INSERT INTO following(user_id) VALUES (NEW.user_id);
INSERT INTO follower(user_id) VALUES (NEW.user_id);
END |
DELIMITER ;

-- A trigger to insert the dish_id into other tables associated with dish
DROP TRIGGER IF EXISTS dish_updater;

DELIMITER |
CREATE TRIGGER dish_updater
AFTER INSERT ON `dish` FOR EACH ROW
BEGIN
AFTER INSERT ON dish FOR EACH ROW
BEGIN
INSERT INTO comment(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_keep(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_like(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_tasted(dish_id) VALUES (NEW.dish_id);
END |
DELIMITER ;

-- A trigger to insert the restaurant_id into other tables associated with restaurant
DROP TRIGGER IF EXISTS restaurant_updater;

DELIMITER |
CREATE TRIGGER restaurant_updater
AFTER INSERT ON `restaurant` FOR EACH ROW
BEGIN
AFTER INSERT ON restaurant FOR EACH ROW
BEGIN
INSERT INTO review(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_keep(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_like(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_visited(restaurant_id) VALUES (NEW.restaurant_id);
END |
DELIMITER ;
