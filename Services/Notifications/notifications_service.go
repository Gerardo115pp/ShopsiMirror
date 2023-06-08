package main

import (
	"context"
	app_config "notifications-service/Config"
	"notifications-service/database"
	"notifications-service/handlers"
	middleware "notifications-service/middlewares"
	"notifications-service/repository"
	"notifications-service/server"

	"github.com/Gerardo115pp/patriot_router"
	"github.com/Gerardo115pp/patriots_lib/echo"
)

func BinderRoutes(server server.Server, router *patriot_router.Router) {
	middleware.SetJWTSecret(app_config.JWT_SECRET)
	router.RegisterRoute(patriot_router.NewRoute("/events", true), middleware.CheckAuth(handlers.EventsHandler(server)))
	router.RegisterRoute(patriot_router.NewRoute("/types", true), middleware.CheckAuth(handlers.EventTypesHandler(server)))

}

func main() {

	app_config.VerifyConfig()

	echo.Echo(echo.GreenFG, "Starting notifications-service")

	var new_server_config *server.ServerConfig = new(server.ServerConfig)
	new_server_config.Port = app_config.NOTIFICATIONS_PORT

	repository.SetEventRepository(database.NewEventsSqliteDB())
	echo.Echo(echo.GreenFG, "Events database connection established")

	new_server, err := server.NewBroker(context.Background(), new_server_config)
	if err != nil {
		echo.Echo(echo.RedFG, "Error creating server broker on [main]: ")
		echo.EchoFatal(err)
	}

	new_server.Run(BinderRoutes)
}
