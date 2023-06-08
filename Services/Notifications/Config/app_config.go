package app_config

import (
	"os"
) // Loads the configuration from the environment variables

var SQLITE_DATABASE_URL string = os.Getenv("NOTIF_DB_URL")
var NOTIFICATIONS_PORT string = os.Getenv("NOTIF_PORT")
var NOTIFICATIONS_DNS string = os.Getenv("NOTIF_DNS")
var JWT_SECRET string = os.Getenv("JWT_SECRET")
var DOMAIN_SECRET string = os.Getenv("DOMAIN_SECRET")

func VerifyConfig() {
	if SQLITE_DATABASE_URL == "" {
		panic("ORD_DB_URL environment variable is required")
	}
	if NOTIFICATIONS_PORT == "" {
		panic("ORD_PORT environment variable is required")
	}
	if NOTIFICATIONS_DNS == "" {
		panic("ORD_DNS environment variable is required")
	}
	if JWT_SECRET == "" {
		panic("JWT_SECRET environment variable is required")
	}
	if DOMAIN_SECRET == "" {
		panic("DOMAIN_SECRET environment variable is required")
	}
}
