package handlers

import (
	"bonhart_oauth_serivce/server"
	"fmt"
	"net/http"

	"github.com/Gerardo115pp/patriots_lib/echo"
)

var jwt_secret string

func SetJWTSecret(secret string) {
	if jwt_secret == "" {
		jwt_secret = secret
	} else {
		echo.EchoFatal(fmt.Errorf("jwt secret is already set"))
	}
}

func JWTKey() string {
	return jwt_secret
}

/* LOGIN USER */

func MeliOauth(orders_server server.Server) http.HandlerFunc {
	return func(response http.ResponseWriter, request *http.Request) {
		switch request.Method {
		case http.MethodGet:
			getTokensHandler(response, request)
		case http.MethodPost:
			postTokensHandler(response, request)
		case http.MethodPatch:
			patchTokensHandler(response, request)
		case http.MethodDelete:
			deleteTokensHandler(response, request)
		case http.MethodPut:
			putTokensHandler(response, request)
		case http.MethodOptions:
			response.WriteHeader(http.StatusOK) // V8 crys really hard and patheticly when you don't return a status code
		default:
			response.WriteHeader(http.StatusMethodNotAllowed)
		}

	}
}

func getTokensHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Get Requests */
	response.WriteHeader(405) // Method not allowed
}

func postTokensHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(405) // Method not allowed
}

func patchTokensHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Patch requests */
	response.WriteHeader(405) // Method not allowed
}

func deleteTokensHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Delete requests */
	response.WriteHeader(405) // Method not allowed
}

func putTokensHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Put requests */
	response.WriteHeader(405) // Method not allowed
}
