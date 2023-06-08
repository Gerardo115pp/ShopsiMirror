.headers ON 
.mode line

CREATE TABLE IF NOT EXISTS `events` (
    `id` TEXT PRIMARY KEY,
    `type` TEXT NOT NULL,
    `description` TEXT NOT NULL,
    `ocurred_at` TEXT NOT NULL,
    `actor` TEXT NOT NULL
);
