package middleware

import (
	"context"
	"fmt"
	"net/http"
	app_config "shopsi_users_service/Config"
	"shopsi_users_service/models"
	"strings"

	"github.com/Gerardo115pp/patriots_lib/echo"
	"github.com/golang-jwt/jwt"
)

var (
	NO_AUTH_NEEDED = map[string][]string{
		"/order": {"GET"}, // don't need to check auth for this route with this method

	}
)

func shouldCheckToken(route string, request_method string) bool {
	if request_method == "OPTIONS" {
		return false
	}

	for no_auth_route, methods := range NO_AUTH_NEEDED {
		if strings.HasPrefix(route, no_auth_route) {
			for _, method := range methods {
				if method == request_method {
					return false
				}
			}
		}
	}

	return true
}

func CheckAuth(next func(response http.ResponseWriter, request *http.Request)) http.HandlerFunc {
	return func(response http.ResponseWriter, request *http.Request) {
		token := request.Header.Get("Authorization")
		echo.Echo(echo.SkyBlueFG, fmt.Sprintf("Checking auth(%s) for route: %s", token, request.URL.Path))
		if token == app_config.DOMAIN_SECRET {
			new_request := request.WithContext(context.WithValue(request.Context(), "user_id", app_config.DOMAIN_SECRET))
			next(response, new_request)
			return
		}

		if !shouldCheckToken(request.URL.Path, request.Method) {
			next(response, request)
			return
		}
		echo.Echo(echo.GreenFG, fmt.Sprintf("Checking auth for %s", request.URL.Path))

		if token == "" {
			token = request.URL.Query().Get("token")
		}

		token = strings.TrimPrefix(token, "Bearer ")
		token = strings.TrimSpace(token)
		if token == "" {
			echo.Echo(echo.RedFG, "No token provided")
			response.WriteHeader(401) // Unauthorized
			return
		}

		token_data, err := jwt.ParseWithClaims(token, &models.AppClaims{}, func(t *jwt.Token) (interface{}, error) {
			return []byte(app_config.JWT_SECRET), nil
		})

		if err != nil {
			echo.Echo(echo.RedFG, fmt.Sprintf("Error parsing token: %s", err.Error()))
			response.WriteHeader(401) // Unauthorized
			return
		}

		var user_data map[string]string = make(map[string]string)
		user_data["user_id"] = token_data.Claims.(*models.AppClaims).UserID
		user_data["username"] = token_data.Claims.(*models.AppClaims).Username
		user_data["email"] = token_data.Claims.(*models.AppClaims).Email
		new_request := request.WithContext(context.WithValue(request.Context(), "user_data", user_data))

		next(response, new_request)
	}
}
