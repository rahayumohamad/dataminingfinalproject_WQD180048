DROP DATABASE IF EXISTS KLSE;
CREATE DATABASE IF NOT EXISTS KLSE;
USE KLSE;

CREATE TABLE `Stock` (
    `stock_name` VARCHAR(30) NOT NULL,
    `stock_code` INTEGER NOT NULL,
    `open_price` FLOAT,
    `high_price` FLOAT,
    `low_price` FLOAT,
    `last_price` FLOAT,
	`price_change` FLOAT,
    `price_change_percent` FLOAT,
	`stock_volume` INTEGER,
	`buy_volume` VARCHAR(30),
	`sell_volume` VARCHAR(30),
	`date` DATETIME
);
