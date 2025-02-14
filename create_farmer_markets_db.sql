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
state varchar(150),
country varchar(150),
city varchar(150),
street varchar(150),

x float,
y float,

Season1Date varchar(200),
Season1Time varchar(200),
Season2Date varchar(200),
Season2Time varchar(200),
Season3Date varchar(200),
Season3Time varchar(200),
Season4Date varchar(200),
Season4Time varchar(200)
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