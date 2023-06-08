package workflows

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	app_config "shopsi_users_service/Config"
	"shopsi_users_service/models"

	"github.com/Gerardo115pp/patriots_lib/echo"
)

func emitEvent(event *models.Event) {
	var err error
	var request *http.Request

	var client *http.Client = new(http.Client)
	var request_body []byte

	request_body, err = json.Marshal(event)
	if err != nil {
		echo.Echo(echo.RedFG, "Error marshalling event [emitEvent]: ")
		echo.EchoErr(err)
		return
	}

	request, err = http.NewRequest("POST", fmt.Sprintf("%s/events", app_config.NOTIFICATIONS_SERVICE), bytes.NewReader(request_body))
	if err != nil {
		echo.Echo(echo.RedBG, "Error creating request for event emision on [emitEvent]: ")
		echo.EchoErr(err)
		return
	}

	request.Header.Set("Content-Type", "application/json")
	request.Header.Set("Authorization", fmt.Sprintf("%s", app_config.DOMAIN_SECRET))

	response, err := client.Do(request)
	if err != nil {
		echo.Echo(echo.RedBG, "Error sending request for event emision on [emitEvent]: ")
		echo.EchoErr(err)
		return
	}

	response.Body.Close()
}

func emitUserLoginEvent(user_identifier string) {
	event := models.CreateEvent(user_identifier, fmt.Sprintf("User %s logged in", user_identifier), models.EventUserLogin)
	emitEvent(event)
}

func emitUserLogoutEvent(user_identifier string) {
	event := models.CreateEvent(user_identifier, fmt.Sprintf("User %s logged out", user_identifier), models.EventUserLogout)
	emitEvent(event)
}

func emitUserCreatedEvent(user_identifier string, description string) {
	event := models.CreateEvent(user_identifier, description, models.EventUserCreated)
	emitEvent(event)
}

func emitUserUpdatedEvent(user_identifier string, description string) {
	event := models.CreateEvent(user_identifier, description, models.EventUserUpdated)
	emitEvent(event)
}

func emitUserDeletedEvent(user_identifier string, description string) {
	event := models.CreateEvent(user_identifier, description, models.EventUserDeleted)
	emitEvent(event)
}
