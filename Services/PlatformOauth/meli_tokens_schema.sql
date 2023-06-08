/* 
  Made for Sqlite3
 */
PRAGMA foreign_keys = ON;
.headers ON

DROP TABLE IF EXISTS `users_oauth_tokens`;
CREATE TABLE `users_oauth_tokens` (
  `code` VARCHAR(255) NOT NULL,
  `redirect_uri` VARCHAR(255) NOT NULL,
  `client_id` VARCHAR(255) NOT NULL,
  `client_secret` VARCHAR(255) NOT NULL,
  `grant_type` VARCHAR(255) NOT NULL,
  `access_token` VARCHAR(255) NOT NULL,
  `token_type` VARCHAR(60) NOT NULL,
  `expires_in` REAL NOT NULL,
  `scope` VARCHAR(255) NOT NULL,
  `refresh_token` VARCHAR(255) NOT NULL,
  `user_id` INT DEFAULT 0,
  `app_usr` VARCHAR(255) NOT NULL
);


