package models

type UserEventType string

const (
	EventUserLogin   UserEventType = "user_login"
	EventUserLogout  UserEventType = "user_logout"
	EventUserCreated UserEventType = "user_created"
	EventUserUpdated UserEventType = "user_updated"
	EventUserDeleted UserEventType = "user_deleted"
)

type Event struct {
	Description string        `json:"description"`
	Type        UserEventType `json:"type"`
	Actor       string        `json:"actor"`
}

func CreateEvent(user_identifier string, description string, event_type UserEventType) *Event {
	return &Event{
		Description: description,
		Type:        event_type,
		Actor:       user_identifier,
	}
}
