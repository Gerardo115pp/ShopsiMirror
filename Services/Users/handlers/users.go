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

const ENABLE_SIGNUP = true

type SignUpRequest struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

type DeleteUserRequest struct {
	Username string `json:"username"`
	Email    string `json:"email"`
}

type PatchUserRequest struct {
	Id       string `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

type HomeResponse struct {
	Message string `json:"message"`
	Status  bool   `json:"status"`
}

func UsersHandler(orders_server server.Server) http.HandlerFunc {
	return func(response http.ResponseWriter, request *http.Request) {
		switch request.Method {
		case "GET":
			getUsersHandler(response, request)
		case "POST":
			postUsersHandler(response, request)
		case "PATCH":
			patchUsersHandler(response, request)
		case "PUT":
			putUsersHandler(response, request)
		case "DELETE":
			deleteUsersHandler(response, request)
		case "OPTIONS":
			response.WriteHeader(200)
		default:
			response.WriteHeader(405)
		}
	}
}

func getUsersHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Get Requests */
	all_users, err := repository.GetAllShopsiUsers(request.Context())
	if err != nil {
		echo.EchoErr(err)
		response.WriteHeader(500)
		return
	}

	response.WriteHeader(200)
	json.NewEncoder(response).Encode(all_users)
}

func postUsersHandler(response http.ResponseWriter, request *http.Request) {
	var signup_request *SignUpRequest
	err := json.NewDecoder(request.Body).Decode(&signup_request)

	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "Internal server error, sorry for the inconvinience", 500)
		return
	}

	if signup_request.Username == "" || signup_request.Email == "" || signup_request.Password == "" {
		echo.EchoErr(fmt.Errorf("missing username, email or password"))
		http.Error(response, "Missing required fields", 400)
	}

	var new_shopsi_user *models.ShopsiUser = models.CreateShopsiUserObject(signup_request.Email, signup_request.Password, signup_request.Username)

	var user_exists bool = repository.UserExists(request.Context(), new_shopsi_user)
	echo.EchoWarn(fmt.Sprintf("user exists: %t", user_exists))
	if user_exists {
		echo.EchoErr(fmt.Errorf("user already exists"))
		http.Error(response, "User already exists", 409)
		return
	}

	err = repository.InsertShopsiUser(request.Context(), new_shopsi_user)
	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "Internal server error, sorry for the inconvinience", 500)
	}

	response.Header().Set("Content-Type", "application/json")
	response.WriteHeader(201)

	var creator map[string]string = request.Context().Value("user_data").(map[string]string)
	workflows.Events.EmitUserCreatedEvent(creator["email"], fmt.Sprintf("'%s' created new user with email '%s'", creator["username"], new_shopsi_user.Email))
}

func patchUsersHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Patch Requests */
	var patch_request *PatchUserRequest

	err := json.NewDecoder(request.Body).Decode(&patch_request)
	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "Unprocessable request body", 422)
		return
	}

	var target_user *models.ShopsiUser
	target_user, err = repository.GetShopsiUserByID(request.Context(), patch_request.Id)

	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "Probably the user does not exist", 404)
		return
	}

	if patch_request.Username != "" && patch_request.Username != target_user.Username {
		target_user.Username = patch_request.Username
	}

	if patch_request.Email != "" && patch_request.Email != target_user.Email {
		target_user.Email = patch_request.Email
	}

	if patch_request.Password != "" {
		// user password must be rehashed
		target_user.Password = models.HashUserPassword(patch_request.Password)
	}

	err = repository.UpdateShopsiUser(request.Context(), target_user)
	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "Internal server error, sorry for the inconvinience", 500)
		return
	}

	response.WriteHeader(202)

	var creator map[string]string = request.Context().Value("user_data").(map[string]string)
	workflows.Events.EmitUserUpdatedEvent(creator["email"], fmt.Sprintf("'%s' updated user with email '%s'", creator["username"], target_user.Email))
}

func putUsersHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Put Requests */
	response.WriteHeader(405) // Method not allowed
}

func deleteUsersHandler(response http.ResponseWriter, request *http.Request) {
	/* Handle Delete Requests */
	var delete_request *DeleteUserRequest

	err := json.NewDecoder(request.Body).Decode(&delete_request)
	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "Incorrect request body", 400)
		return
	}

	if delete_request.Username == "" || delete_request.Email == "" {
		echo.EchoErr(fmt.Errorf("missing username or email"))
		http.Error(response, "Missing required fields", 406)
		return
	}

	err = repository.DeleteShopsiUser(request.Context(), delete_request.Username, delete_request.Email)

	if err != nil {
		echo.EchoErr(err)
		http.Error(response, "Internal server error, sorry for the inconvinience", 500)
		return
	}

	response.WriteHeader(200)

	var creator map[string]string = request.Context().Value("user_data").(map[string]string)
	workflows.Events.EmitUserDeletedEvent(creator["email"], fmt.Sprintf("'%s' deleted user with email '%s'", creator["username"], delete_request.Email))
}
