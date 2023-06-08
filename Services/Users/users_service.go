package main

import (
	"context"
	"fmt"
	app_config "shopsi_users_service/Config"
	"shopsi_users_service/database"
	"shopsi_users_service/handlers"
	middleware "shopsi_users_service/middlewares"
	"shopsi_users_service/repository"
	"shopsi_users_service/server"

	"github.com/Gerardo115pp/patriot_router"
	"github.com/Gerardo115pp/patriots_lib/echo"
)

func BinderRoutes(server server.Server, router *patriot_router.Router) {
	if handlers.JWTKey() == "" {
		handlers.SetJWTSecret(server.Config().JWTKey)
	}

	router.RegisterRoute(patriot_router.NewRoute("/users", true), middleware.CheckAuth(handlers.UsersHandler(server)))
	router.RegisterRoute(patriot_router.NewRoute("/tokens(/[a-z_]{2,10})?", false), handlers.ShopsiUserTokensHandler(server))
}

func main() {

	app_config.VerifyConfig()

	echo.Echo(echo.GreenFG, "Starting shopsi_auth_service")
	echo.EchoDebug(fmt.Sprintf("DB URL: %s", app_config.SQLITE_DATABASE_URL))

	var new_server_config *server.ServerConfig = new(server.ServerConfig)
	new_server_config.Port = app_config.USERS_PORT
	new_server_config.JWTKey = app_config.JWT_SECRET
	new_server_config.DatabaseURL = app_config.SQLITE_DATABASE_URL

	auth_repository, err := database.NewSQLite3Repository(app_config.SQLITE_DATABASE_URL)

	repository.SetShopsiUserRepository(auth_repository)

	echo.EchoDebug(fmt.Sprintf("server config: %+v", new_server_config))

	server, err := server.NewBroker(context.Background(), new_server_config)
	if err != nil {
		echo.EchoFatal(err)
	}

	server.Run(BinderRoutes)

}
