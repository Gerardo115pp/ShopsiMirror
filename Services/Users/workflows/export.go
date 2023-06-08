package workflows

type eventMethods struct {
	EmitUserLoginEvent   func(user_identifier string)
	EmitUserLogoutEvent  func(user_identifier string)
	EmitUserCreatedEvent func(user_identifier string, description string)
	EmitUserUpdatedEvent func(user_identifier string, description string)
	EmitUserDeletedEvent func(user_identifier string, description string)
}

var Events *eventMethods = &eventMethods{
	EmitUserLoginEvent:   emitUserLoginEvent,
	EmitUserLogoutEvent:  emitUserLogoutEvent,
	EmitUserCreatedEvent: emitUserCreatedEvent,
	EmitUserUpdatedEvent: emitUserUpdatedEvent,
	EmitUserDeletedEvent: emitUserDeletedEvent,
}
