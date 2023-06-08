DROP DATABASE IF EXISTS `tracked_products`;
CREATE DATABASE IF NOT EXISTS `tracked_products`;
USE `tracked_products`;

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
    `meli_id` VARCHAR(15) UNIQUE,
    `name` VARCHAR(255),
    `site_id` VARCHAR(10),
    `category_id` VARCHAR(10),
    `initial_price` INT NOT NULL,
    `secure_thumbnail` VARCHAR(255),
    `condition` VARCHAR(20),
    `sku` VARCHAR(20) NOT NULL,
    `status` VARCHAR(30),
    `competes_with` VARCHAR(20),
    `meli_url` VARCHAR(255),
    `domain_id` VARCHAR(120),
    `seller_id` INT NOT NULL,
    `type` ENUM('user', 'competitor', 'tracked') DEFAULT 'competitor',
    `product_id` VARCHAR(40) DEFAULT (SHA1(CONCAT(`seller_id`, '-', `meli_id`))),
    PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `sellers`;
CREATE TABLE `sellers` (
    `seller_id` INT NOT NULL PRIMARY KEY,
    `nickname` VARCHAR(255),
    `meli_profile_link` VARCHAR(255),
    `added_date` DATETIME DEFAULT NOW(),
    `meli_registration_date` DATETIME    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `products` ADD CONSTRAINT `fk_seller_id` FOREIGN KEY (`seller_id`) REFERENCES `sellers` (`seller_id`) ON DELETE CASCADE;

DROP VIEW IF EXISTS `our_products`;
CREATE VIEW `our_products` AS SELECT * FROM `products` WHERE `seller_id`=266839332; /* Shopsi id in meli */

DROP VIEW IF EXISTS `competitors_products`;
CREATE VIEW `competitors_products` AS SELECT * FROM `products` WHERE `seller_id`!=266839332 AND `type`='competitor';

DROP TABLE IF EXISTS `sellers_reputations`; 
CREATE TABLE `sellers_reputations` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `power_seller_status` VARCHAR(50),
    `recorded_date` DATETIME DEFAULT NOW(),
    `cancelled_transactions` INT UNSIGNED ,
    `total_transactions` INT UNSIGNED ,
    `completed_transactions` INT UNSIGNED GENERATED ALWAYS AS (`total_transactions` - `cancelled_transactions`),
    `positive_ratings` DECIMAL(3,2) NOT NULL,
    `negative_ratings` DECIMAL(3,2) NOT NULL,
    `neutral_ratings` DECIMAL(3,2) NOT NULL,
    `level` VARCHAR(20) NOT NULL,
    `seller_id` INT NOT NULL,
    CONSTRAINT `fk_seller_rep` FOREIGN KEY (`seller_id`) REFERENCES `sellers` (`seller_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP VIEW IF EXISTS `our_reputations`;
CREATE VIEW `our_reputations` AS SELECT * FROM `sellers_reputations` WHERE `seller_id`=266839332; /* Shopsi id in meli */

DROP TABLE IF EXISTS `product_performance_records`;
CREATE TABLE `product_performance_records` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `recorded_date` DATETIME DEFAULT NOW(),
    `serial` INT UNSIGNED NOT NULL, 
    `visits` INT DEFAULT -1,
    `sales`  INT DEFAULT -1,
    `current_price` INT DEFAULT -1,
    `stock` INT UNSIGNED NOT NULL,
    `has_discount` TINYINT(1) DEFAULT 0,
    `measures` VARCHAR(40) NOT NULL,
    `is_completed` TINYINT(1) GENERATED ALWAYS AS (`visits`!=-1 AND `sales`!=-1 AND `current_price`!=-1 AND `stock`!=-1) VIRTUAL,
    CONSTRAINT `fk_product_id` FOREIGN KEY (`measures`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- serial is the identifier of the current performance record batch

DROP TRIGGER IF EXISTS `check_performance_record_duplicates`;
DELIMITER //
CREATE TRIGGER `check_performance_record_duplicates` BEFORE INSERT ON `product_performance_records` FOR EACH ROW
BEGIN
    SET @other = (select id from product_performance_records where serial=NEW.serial and measures=NEW.measures);
    IF @other IS NOT NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate record';
    END IF;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS `set_product_type`;
DELIMITER //
CREATE TRIGGER `set_product_type` BEFORE INSERT ON `products` FOR EACH ROW
BEGIN
    IF NEW.seller_id=266839332 THEN
        SET NEW.type='user';
    ELSEIF NEW.type!='tracked' THEN
        SET NEW.type='competitor';
    END IF;
END//

DROP VIEW IF EXISTS `missing_performance_records`; /* The products that dont have a performance record on the current batch and are active */
CREATE VIEW `missing_performance_records` AS SELECT `meli_id`, `product_id`, `meli_url` FROM `products` WHERE status='active' AND `product_id` NOT IN (SELECT `measures` FROM `product_performance_records` WHERE `serial`=(SELECT MAX(`serial`) FROM `product_performance_records`));

DROP VIEW IF EXISTS `performance`;
CREATE VIEW `performance` AS select `p`.`meli_id` AS `meli_id` ,`p`.`name` AS `name`,`p`.`initial_price` AS `initial_price`,`p`.`condition` AS `condition`,`p`.`sku` AS `sku`,`p`.`status` AS `status`,`p`.`competes_with` = '' AS `is_ours`,`p`.`meli_url` AS `meli_url`,`pr`.`recorded_date` AS `recorded`,`pr`.`visits` AS `visits`,`pr`.`sales` AS `sales`,`pr`.`current_price` AS `current_price`,`pr`.`stock` AS `stock`,`pr`.`has_discount` AS `has_discount` from `products` `p` left join `product_performance_records` `pr` on `p`.`product_id`=`pr`.`measures` where `pr`.`serial`=(select max(`serial`) from `product_performance_records`);

DROP VIEW IF EXISTS `performance_reports`;
CREATE VIEW `performance_reports` AS SELECT MAX(`recorded_date`) AS `last_update`, `serial`, COUNT(`serial`) AS `records`, COUNT(IF(`is_completed`=1, 1, NULL)) AS `completed` FROM `product_performance_records` GROUP BY `serial`;