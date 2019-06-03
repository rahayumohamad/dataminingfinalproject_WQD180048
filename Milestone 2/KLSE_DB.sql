############################################################################################
#                                                                                          #
#      This code is written during team meet-up by team members as shown below ...         #
#                                                                                          #  
#                    HAFIFI BIN YAHYA - WQD170042                                          #
#                    NOR ASMIDAH BINTI MOHD ARSHAD - WQD180006                             #
#                    MAS RAHAYU BINTI MOHAMAD - WQD180048                                  #
#                    LEE CHUN MUN - WQD180066                                              #
#                    JOJIE ANAK NANJU - WQD180029                                          #
#                                                                                          #
############################################################################################

 
DROP DATABASE IF EXISTS KLSE;
CREATE DATABASE IF NOT EXISTS KLSE;
USE KLSE;

CREATE TABLE `Main_Listed_Companies` (
	`stock_name` VARCHAR(10) NOT NULL,
	`stock_code` VARCHAR(10) NOT NULL,
    `business_area` VARCHAR(60),
	`company_name` varchar(60),
	`known_name` VARCHAR(60),
	CONSTRAINT `PK_Main_Listed_Companies` PRIMARY KEY (`stock_code`, `stock_name`)
);

CREATE TABLE `Stock` (
    `stock_name` VARCHAR(10) NOT NULL,
    `stock_code` VARCHAR(10) NOT NULL,
    `open_price` FLOAT,
    `high_price` FLOAT,
    `low_price` FLOAT,
    `last_price` FLOAT,
	`price_change` FLOAT,
    `price_change_percent` FLOAT,
	`stock_volume` INTEGER,
	`buy_volume` VARCHAR(30),
	`sell_volume` VARCHAR(30),
	`date` DATETIME NOT NULL
);

CREATE TABLE `Quater_Reports` (
    `stock_code` VARCHAR(10) NOT NULL,
    `EPS` VARCHAR(20),
    `DPS` VARCHAR(20),
    `NTA` VARCHAR(20),
    `Revenue` VARCHAR(20),
    `PL` VARCHAR(20),
    `Quarter` VARCHAR(4),
    `Q_Year` VARCHAR(4)
);

CREATE TABLE `News_Announcement_Links` (
    `stock_code` VARCHAR(10) NOT NULL,
	`main_site` VARCHAR(200),
	`weblink` VARCHAR(200)
);

CREATE TABLE `News_Announcement_Extraction` (
    `stock_code` VARCHAR(10) NOT NULL,
	`link` VARCHAR(400),
	`news_details` VARCHAR(3000)
);

CREATE TABLE `Twitter` (
    `tweet_id` VARCHAR(20) NOT NULL,
	`screen_name` VARCHAR(60),
	`created_at` DATETIME,
	`text` VARCHAR(3000)
);