CREATE SCHEMA IF NOT EXISTS "markets"
AUTHORIZATION postgres;

create table markets.markets
(
FMID int PRIMARY KEY,
market_name varchar(100) NOT NULL,

website varchar(200),
facebook varchar(200),
twitter varchar(200),
youtube varchar(200),
other_media varchar(200),

zip varchar(150),
street varchar(150),

x float,
y float
);

CREATE TABLE markets.users
(
    user_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_nickname text NOT NULL UNIQUE,
    password_hash text NOT NULL
);

CREATE TABLE markets.comments
(
    FMID int NOT NULL,
    user_id int NOT NULL,
    PRIMARY KEY (FMID, user_id),

    FOREIGN KEY (FMID) REFERENCES markets.markets(FMID) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES markets.users(user_id) ON DELETE CASCADE
);

CREATE TABLE markets.states
(
    state_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    state_name text NOT NULL UNIQUE
);

CREATE TABLE markets.market_state
(
    FMID int NOT NULL,
    state_id int NOT NULL,
    PRIMARY KEY (FMID, state_id),
    FOREIGN KEY (FMID) REFERENCES markets.markets(FMID) ON DELETE CASCADE,
    FOREIGN KEY (state_id) REFERENCES markets.states(state_id) ON DELETE CASCADE
);

CREATE TABLE markets.countries
(
    country_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country_name text NOT NULL UNIQUE
);

CREATE TABLE markets.market_country
(
    FMID int NOT NULL,
    country_id int NOT NULL,
    PRIMARY KEY (FMID, country_id),
    FOREIGN KEY (FMID) REFERENCES markets.markets(FMID) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES markets.countries(country_id) ON DELETE CASCADE
);

CREATE TABLE markets.cities
(
    city_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city_name text NOT NULL UNIQUE
);

CREATE TABLE markets.market_city
(
    FMID int NOT NULL,
    city_id int NOT NULL,
    PRIMARY KEY (FMID, city_id),
    FOREIGN KEY (FMID) REFERENCES markets.markets(FMID) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES markets.cities(city_id) ON DELETE CASCADE
);

CREATE TABLE markets.products
(
    product_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  
    product_name text NOT NULL UNIQUE
);

CREATE TABLE markets.payment_methods
(
    payment_method_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  
    payment_method text NOT NULL UNIQUE
);

CREATE TABLE markets.markets_payment_methods (
    FMID int NOT NULL,
    payment_method_id int NOT NULL,
    PRIMARY KEY (FMID, payment_method_id),
    FOREIGN KEY (FMID) REFERENCES markets.markets(FMID) ON DELETE CASCADE,
    FOREIGN KEY (payment_method_id) REFERENCES markets.payment_methods(payment_method_id) ON DELETE CASCADE
);

CREATE TABLE markets.markets_products (
    FMID int NOT NULL,
    product_id int NOT NULL,
    PRIMARY KEY (FMID, product_id),
    FOREIGN KEY (FMID) REFERENCES markets.markets(FMID) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES markets.products(product_id) ON DELETE CASCADE
);