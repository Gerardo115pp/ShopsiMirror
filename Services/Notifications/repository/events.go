package repository

import (
	"context"
	"fmt"
	"notifications-service/models"

	"github.com/Gerardo115pp/patriots_lib/echo"
)

type EventRepository interface {
	InsertEvent(ctx context.Context, event *models.Event) error
	FindAllEvents(ctx context.Context) ([]*models.Event, error)
	FindEventByID(ctx context.Context, id string) (*models.Event, error)
	FindEventsByType(ctx context.Context, event_type models.EventType) ([]*models.Event, error)
	FindEventsByActor(ctx context.Context, user_id string) ([]*models.Event, error)
	Close()
}

type eventRepository struct {
	repo EventRepository
}

func (event_repo eventRepository) checkRepoSet() {
	if event_repo.repo == nil {
		echo.EchoFatal(fmt.Errorf("Event repository is nil"))
	}
}

func (event_repo *eventRepository) InsertEvent(ctx context.Context, event *models.Event) error {
	event_repo.checkRepoSet() // panics if repo is nil

	return event_repo.repo.InsertEvent(ctx, event)
}

func (event_repo *eventRepository) FindAllEvents(ctx context.Context) ([]*models.Event, error) {
	event_repo.checkRepoSet() // panics if repo is nil
	return event_repo.repo.FindAllEvents(ctx)
}

func (event_repo *eventRepository) FindEventByID(ctx context.Context, id string) (*models.Event, error) {
	event_repo.checkRepoSet() // panics if repo is nil

	return event_repo.repo.FindEventByID(ctx, id)
}

func (event_repo *eventRepository) FindEventsByType(ctx context.Context, event_type models.EventType) ([]*models.Event, error) {
	event_repo.checkRepoSet() // panics if repo is nil
	return event_repo.repo.FindEventsByType(ctx, event_type)
}

func (event_repo *eventRepository) FindEventsByUser(ctx context.Context, user_id string) ([]*models.Event, error) {
	event_repo.checkRepoSet() // panics if repo is nil

	return event_repo.repo.FindEventsByActor(ctx, user_id)
}

func (event_repo *eventRepository) Close() {
	event_repo.checkRepoSet() // panics if repo is nil
	event_repo.repo.Close()
}

var Events *eventRepository = new(eventRepository)

func SetEventRepository(repo EventRepository) {
	Events.repo = repo
}
