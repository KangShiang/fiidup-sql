--#######################################################--
--# This is the sql script to setup the fiidup SQL      #--
--# database with all necessary tables and constraints  #--
--#######################################################--

-- ###### TABLES FOR DISHES ###### --
CREATE TABLE IF NOT EXISTS dish2
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

CREATE TABLE IF NOT EXISTS comment2
(
comment_id int NOT NULL AUTO_INCREMENT,
dish_id int NOT NULL,
comment text NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (comment_id),
FOREIGN KEY (dish_id) REFERENCES dish2(dish_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_keep2
(
dish_id int NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (dish_id),
FOREIGN KEY (dish_id) REFERENCES dish2(dish_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_like2
(
dish_id int NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (dish_id),
FOREIGN KEY (dish_id) REFERENCES dish2(dish_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dish_tasted2
(
dish_id int NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (dish_id),
FOREIGN KEY (dish_id) REFERENCES dish2(dish_id) ON DELETE CASCADE
);

-- ###### TABLES FOR RESTAURANTS ###### --
CREATE TABLE IF NOT EXISTS restaurant2
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

CREATE TABLE IF NOT EXISTS review2
(
review_id int NOT NULL AUTO_INCREMENT,
restaurant_id int NOT NULL,
user_id text NOT NULL,
review text NOT NULL,
PRIMARY KEY (review_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant2(restaurant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS restaurant_keep2
(
restaurant_id int NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (restaurant_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant2(restaurant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS restaurant_like2
(
restaurant_id int NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (restaurant_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant2(restaurant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS restaurant_visited2
(
restaurant_id int NOT NULL,
user_id text NOT NULL,
PRIMARY KEY (restaurant_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant2(restaurant_id) ON DELETE CASCADE
);

-- ###### TRIGGERS ###### --

-- A trigger to insert the dish_id into other tables associated with dish
DELIMITER |
CREATE TRIGGER dish_updater
AFTER INSERT ON `dish2` FOR EACH ROW
BEGIN
INSERT INTO comment2(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_keep2(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_like2(dish_id) VALUES (NEW.dish_id);
INSERT INTO dish_tasted2(dish_id) VALUES (NEW.dish_id);
END |
DELIMITER ;

-- A trigger to insert the restaurant_id into other tables associated with restaurant
DELIMITER |
CREATE TRIGGER restaurant_updater
AFTER INSERT ON `restaurant2` FOR EACH ROW
BEGIN
INSERT INTO review2(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_keep2(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_like2(restaurant_id) VALUES (NEW.restaurant_id);
INSERT INTO restaurant_visited2(restaurant_id) VALUES (NEW.restaurant_id);
END |
DELIMITER ;
