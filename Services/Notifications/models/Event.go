package models

import (
	"fmt"
	"time"

	"github.com/Gerardo115pp/patriots_lib/echo"
	"github.com/google/uuid"
)

type EventType string

const (
	EventUserLogin                     EventType = "user_login"
	EventUserLogout                    EventType = "user_logout"
	EventUserCreated                   EventType = "user_created"
	EventUserUpdated                   EventType = "user_updated"
	EventUserDeleted                   EventType = "user_deleted"
	EventProductAdded                  EventType = "product_added"
	EventProductUpdated                EventType = "product_updated"
	EventRapidReportRequested          EventType = "rapid_report_requested"
	EventRapidReportCreated            EventType = "rapid_report_created"
	EventPerformanceReportStarted      EventType = "performance_report_started"
	EventPerformanceReportFinished     EventType = "performance_report_finished"
	EventProductsDatabaseStatusUpdated EventType = "products_database_status_updated"
	EventProductSearchPerformed        EventType = "product_search_performed"
	EventProductCompetitorsUpdated     EventType = "product_competitors_updated"
	EventProductCompetitorPriceDrop    EventType = "product_competitor_price_drop"
	EventProductPositioningChanged     EventType = "product_positioning_changed"
)

func EventTypes() []EventType {
	return []EventType{
		EventUserLogin,
		EventUserLogout,
		EventUserCreated,
		EventUserUpdated,
		EventUserDeleted,
		EventProductAdded,
		EventProductUpdated,
		EventRapidReportRequested,
		EventRapidReportCreated,
		EventPerformanceReportStarted,
		EventPerformanceReportFinished,
		EventProductsDatabaseStatusUpdated,
		EventProductSearchPerformed,
		EventProductCompetitorsUpdated,
		EventProductCompetitorPriceDrop,
		EventProductPositioningChanged,
	}
}

/* CHANGE: events types should be defined in a config file  */

type Event struct {
	ID          string    `json:"id"`
	Description string    `json:"description"`
	OcurredAt   string    `json:"ocurred_at"`
	Type        EventType `json:"type"`
	Actor       string    `json:"actor"`
}

func createEventType(type_string string) (event_type EventType, err error) {
	event_type = EventType(type_string)

	switch event_type {
	case EventUserLogin:
	case EventUserLogout:
	case EventUserCreated:
	case EventUserUpdated:
	case EventUserDeleted:
	case EventProductAdded:
	case EventProductUpdated:
	case EventRapidReportRequested:
	case EventRapidReportCreated:
	case EventPerformanceReportStarted:
	case EventPerformanceReportFinished:
	case EventProductsDatabaseStatusUpdated:
	case EventProductSearchPerformed:
	case EventProductCompetitorsUpdated:
	case EventProductCompetitorPriceDrop:
	case EventProductPositioningChanged:
	default:
		echo.EchoWarn(fmt.Sprintf("Invalid event type: %s", type_string))
	}

	return
}

func CreateEvent(description string, eventType string, actor_identifier string) *Event {
	var event_type EventType
	var new_event *Event = new(Event)

	event_type, err := createEventType(eventType)
	if err != nil {
		echo.Echo(echo.RedFG, "On CreateEvent: ")
		echo.EchoErr(err)
	}

	new_event.ID = fmt.Sprintf("event-%s-%s", eventType, uuid.New().String())
	new_event.OcurredAt = time.Now().Format("2006-01-02 15:04:05")
	new_event.Description = description
	new_event.Actor = actor_identifier
	new_event.Type = event_type

	return new_event
}
