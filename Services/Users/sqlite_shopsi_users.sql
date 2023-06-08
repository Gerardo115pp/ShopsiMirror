PRAGMA foreign_keys = ON;
.headers ON

DROP TABLE IF EXISTS `shopsi_users`;
CREATE TABLE `shopsi_users` (
  `id` TEXT,
  `username` TEXT NOT NULL UNIQUE,
  `email` TEXT NOT NULL UNIQUE,
  `password` TEXT NOT NULL,
  `created_at` TEXT DEFAULT CURRENT_TIMESTAMP
);



