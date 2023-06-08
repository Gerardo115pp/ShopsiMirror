package main

import (
	"bonhart_oauth_serivce/database"
	"bonhart_oauth_serivce/handlers"
	"bonhart_oauth_serivce/repository"
	"bonhart_oauth_serivce/server"
	"context"
	"fmt"
	"os"

	"github.com/Gerardo115pp/patriot_router"
	"github.com/Gerardo115pp/patriots_lib/echo"
)

func BinderRoutes(server server.Server, router *patriot_router.Router) {
	if handlers.JWTKey() == "" {
		handlers.SetJWTSecret(server.Config().JWTKey)
	}

	router.RegisterRoute(patriot_router.NewRoute("/", true), handlers.MeliOauth(server))
}

func main() {

	port := os.Getenv("OAUTH_PORT")
	if port == "" {
		port = ":5050"
	}

	jwt_secret := os.Getenv("JWT_SECRET")
	if jwt_secret == "" {
		jwt_secret = "secret"
	}

	db_url := os.Getenv("OAUTH_DB_URL")
	if db_url == "" {
		echo.EchoFatal(fmt.Errorf("database url is required"))
	}

	echo.Echo(echo.GreenFG, "Starting shopsi_auth_service")
	echo.EchoDebug(fmt.Sprintf("DB URL: %s", db_url))

	var new_server_config *server.ServerConfig = new(server.ServerConfig)
	new_server_config.Port = port
	new_server_config.JWTKey = jwt_secret
	new_server_config.DatabaseURL = db_url

	oauth_repository, err := database.NewSQLite3Repository(db_url)

	repository.SetRepository(oauth_repository)

	echo.EchoDebug(fmt.Sprintf("server config: %+v", new_server_config))

	server, err := server.NewBroker(context.Background(), new_server_config)
	if err != nil {
		echo.EchoFatal(err)
	}

	server.Run(BinderRoutes)

}
