package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"shopsi_users_service/models"
	"shopsi_users_service/repository"
	"shopsi_users_service/server"
	"shopsi_users_service/workflows"

	"github.com/Gerardo115pp/patriots_lib/echo"
	"golang.org/x/crypto/bcrypt"
)

/* LOGIN USER */

type CustomerLoginRequest struct {
	Email    string `json:"email"`
	Username string `json:"username"`
	Password string `json:"password"`
}

type ShopsiUserLoginResponse struct {
	Token string `json:"token"`
	Ok    bool   `json:"ok"`
}

func ShopsiUserTokensHandler(orders_server server.Server) http.HandlerFunc {
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
	var login_request CustomerLoginRequest
	var target_user *models.ShopsiUser
	err := json.NewDecoder(request.Body).Decode(&login_request)
	if err != nil {
		echo.EchoErr(err)
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	if login_request.Password == "" {
		response.WriteHeader(406) // Not acceptable
		echo.EchoWarn("Password is empty")
		return
	}

	if login_request.Email != "" {
		echo.EchoWarn("Client tried to login with email")
		http.Error(response, "Email login is not supported", 410) // Gone, email login is not supported anymore
		return
	}

	if login_request.Username == "" {
		echo.EchoErr(fmt.Errorf("Username is empty"))
		response.WriteHeader(406) // Not acceptable
		return
	}

	echo.EchoDebug(fmt.Sprintf("Trying to login with username: %s", login_request.Username))
	target_user, err = repository.GetShopsiUserByUsername(request.Context(), login_request.Username)
	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "User not found", 404) // Not found
		return
	}

	err = bcrypt.CompareHashAndPassword([]byte(target_user.Password), []byte(login_request.Password))
	if err != nil {
		/* Password is wrong */

		echo.Echo(echo.RedFG, fmt.Sprintf("Password is wrong for user %s", login_request.Username))
		response.WriteHeader(401)
		return
	}

	echo.Echo(echo.GreenFG, fmt.Sprintf("User with %s logged in", login_request.Username))
	token, err := models.CreateToken(target_user, JWTKey())
	if err != nil {
		http.Error(response, "Internal server error", 500)
		echo.EchoErr(err)
		return
	}

	var login_response *ShopsiUserLoginResponse = new(ShopsiUserLoginResponse)
	login_response.Ok = true
	login_response.Token = token
	response.WriteHeader(200)
	json.NewEncoder(response).Encode(login_response)

	workflows.Events.EmitUserLoginEvent(target_user.Email)
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
