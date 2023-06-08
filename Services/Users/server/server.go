package server // change the name of the package depending type of service

import (
	"context"
	"fmt"
	"net/http"
	"shopsi_users_service/repository"

	"github.com/Gerardo115pp/patriot_router"
	"github.com/Gerardo115pp/patriots_lib/echo"
)

type ServerConfig struct {
	Port        string
	JWTKey      string
	DatabaseURL string
}

type Server interface {
	Config() *ServerConfig
}

type Broker struct {
	config *ServerConfig
	router *patriot_router.Router
}

func (broker *Broker) Config() *ServerConfig {
	return broker.config
}

func CorsAllowAll(handler func(http.ResponseWriter, *http.Request)) http.HandlerFunc {
	return func(response http.ResponseWriter, request *http.Request) {
		response.Header().Set("Access-Control-Allow-Origin", "*")
		response.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE, PATCH")
		response.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		handler(response, request)
	}
}

func (broker *Broker) Run(binder func(server Server, router *patriot_router.Router)) {

	broker.router = patriot_router.CreateRouter()
	broker.router.SetCorsHandler(CorsAllowAll)
	binder(broker, broker.router)

	echo.Echo(echo.GreenBG, "Started Auth data service on port "+broker.config.Port)
	if err := http.ListenAndServe(broker.config.Port, broker.router); err != nil {
		echo.EchoFatal(err)
	} else {
		echo.Echo(echo.GreenFG, "Server stopped")
	}

	repository.Close()

}

func NewBroker(ctx context.Context, config *ServerConfig) (*Broker, error) {
	if config.Port == "" {
		return nil, fmt.Errorf("port is required")
	}

	if config.JWTKey == "" {
		return nil, fmt.Errorf("jwt key is required")
	}

	if config.DatabaseURL == "" {
		return nil, fmt.Errorf("database url is required")
	}

	var new_broker *Broker = new(Broker)
	new_broker.config = config
	patriot_router.CreateRouter()

	return new_broker, nil
}
