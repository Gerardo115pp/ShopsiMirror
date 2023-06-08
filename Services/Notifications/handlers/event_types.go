package handlers

import (
	"encoding/json"
	"net/http"
	"notifications-service/models"
	"notifications-service/server"
)

func EventTypesHandler(http_server server.Server) http.HandlerFunc {
	return func(response http.ResponseWriter, request *http.Request) {
		switch request.Method {
		case http.MethodGet:
			getEventTypesHandler(response, request)
		case http.MethodPost:
			postEventTypesHandler(response, request)
		case http.MethodPatch:
			patchEventTypesHandler(response, request)
		case http.MethodDelete:
			deleteEventTypesHandler(response, request)
		case http.MethodPut:
			putEventTypesHandler(response, request)
		case http.MethodOptions:
			response.WriteHeader(http.StatusOK)
		default:
			response.WriteHeader(http.StatusMethodNotAllowed)
		}
	}
}

/* GET */

func getEventTypesHandler(response http.ResponseWriter, request *http.Request) {
	var event_types []models.EventType = models.EventTypes()

	response.Header().Set("Content-Type", "application/json")
	response.WriteHeader(http.StatusOK)
	json.NewEncoder(response).Encode(event_types)
}

/* POST */

func postEventTypesHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(405)
}

/* PUT */

func putEventTypesHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(405)
}

/* DELETE */

func deleteEventTypesHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(405)
}

/* PATCH */

func patchEventTypesHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(405)
}
