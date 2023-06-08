package app_config

import (
	"os"
) // Loads the configuration from the environment variables

var SQLITE_DATABASE_URL string = os.Getenv("USERS_DB_URL")
var USERS_PORT string = os.Getenv("USERS_PORT")
var USERS_DNS string = os.Getenv("USERS_DNS")
var JWT_SECRET string = os.Getenv("JWT_SECRET")
var NOTIFICATIONS_SERVICE string = os.Getenv("INTERNAL_NOTIFICATIONS_SERVER")
var DOMAIN_SECRET string = os.Getenv("DOMAIN_SECRET")

func VerifyConfig() {
	if SQLITE_DATABASE_URL == "" {
		panic("SQLITE_DATABASE_URL environment variable is required")
	}
	if USERS_PORT == "" {
		panic("ORD_PORT environment variable is required")
	}
	if USERS_DNS == "" {
		panic("USERS_PORT environment variable is required")
	}
	if JWT_SECRET == "" {
		panic("JWT_SECRET environment variable is required")
	}
	if NOTIFICATIONS_SERVICE == "" {
		panic("INTERNAL_NOTIFICATIONS_SERVER environment variable is required")
	}
	if DOMAIN_SECRET == "" {
		panic("DOMAIN_SECRET environment variable is required")
	}
}
