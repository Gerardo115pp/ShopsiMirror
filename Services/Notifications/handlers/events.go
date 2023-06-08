package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"notifications-service/models"
	"notifications-service/repository"
	"notifications-service/server"

	"github.com/Gerardo115pp/patriots_lib/echo"
)

type PostEventRequest struct {
	Description string `json:"description"`
	Type        string `json:"type"`
	Actor       string `json:"actor"`
}

func EventsHandler(http_server server.Server) http.HandlerFunc {
	return func(response http.ResponseWriter, request *http.Request) {
		switch request.Method {
		case http.MethodGet:
			getEventsHandler(response, request)
		case http.MethodPost:
			postEventsHandler(response, request)
		case http.MethodPatch:
			patchEventsHandler(response, request)
		case http.MethodDelete:
			deleteEventsHandler(response, request)
		case http.MethodPut:
			putEventsHandler(response, request)
		case http.MethodOptions:
			response.WriteHeader(http.StatusOK)
		default:
			response.WriteHeader(http.StatusMethodNotAllowed)
		}
	}
}

/* GET */

func getEventsHandler(response http.ResponseWriter, request *http.Request) {
	var event_id string = request.URL.Query().Get("id")
	if event_id == "" {
		/* GET ALL */
		getAllEvents(response, request)
		return
	} else {
		/* GET BY ID */
		echo.EchoErr(fmt.Errorf("Get event by id not implemented"))
		response.WriteHeader(501)
	}
}

func getAllEvents(response http.ResponseWriter, request *http.Request) {
	var events []*models.Event
	echo.Echo(echo.GreenBG, "Getting all events")

	events, err := repository.Events.FindAllEvents(request.Context())
	if err != nil {
		echo.Echo(echo.RedBG, "Error getting all events on [getAllEvents]: ")
		echo.EchoErr(err)
		response.WriteHeader(http.StatusInternalServerError)
		return
	}

	response.Header().Set("Content-Type", "application/json")
	response.WriteHeader(http.StatusOK)
	json.NewEncoder(response).Encode(events)

	echo.Echo(echo.GreenBG, "Successfully got all events")
}

/* POST */

func postEventsHandler(response http.ResponseWriter, request *http.Request) {
	var request_body *PostEventRequest = new(PostEventRequest)

	echo.Echo(echo.GreenBG, "Creating new event")
	err := json.NewDecoder(request.Body).Decode(&request_body)
	if err != nil {
		echo.Echo(echo.RedBG, "Error decoding request on [postEventsHandler]: ")
		echo.EchoErr(err)
		response.WriteHeader(400)
		return
	}

	new_event := models.CreateEvent(request_body.Description, request_body.Type, request_body.Actor)

	echo.Echo(echo.CyanFG, fmt.Sprintf("New event: %s[%s] created on %s", new_event.ID, string(new_event.Type), new_event.OcurredAt))

	err = repository.Events.InsertEvent(request.Context(), new_event)
	if err != nil {
		echo.Echo(echo.RedBG, "Error inserting event on [postEventsHandler]: ")
		echo.EchoErr(err)
		response.WriteHeader(500)
		return
	}

	echo.Echo(echo.GreenBG, "Successfully created new event")
	response.WriteHeader(201)
}

/* PUT */

func putEventsHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(http.StatusMethodNotAllowed)
}

/* DELETE */

func deleteEventsHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(http.StatusMethodNotAllowed)
}

/* PATCH */

func patchEventsHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(http.StatusMethodNotAllowed)
}
