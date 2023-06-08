package database

import (
	"context"
	"database/sql"
	app_config "notifications-service/Config"
	"notifications-service/models"

	"github.com/Gerardo115pp/patriots_lib/echo"
	_ "github.com/mattn/go-sqlite3"
)

type EventsSqliteDB struct {
	db *sql.DB
}

func NewEventsSqliteDB() *EventsSqliteDB {
	db, err := sql.Open("sqlite3", app_config.SQLITE_DATABASE_URL)
	if err != nil {
		echo.EchoErr(err)
		return nil
	}

	return &EventsSqliteDB{db: db}
}

func (sqlite *EventsSqliteDB) InsertEvent(ctx context.Context, event *models.Event) error {
	stmt, err := sqlite.db.PrepareContext(ctx, "INSERT INTO events (id, type, actor, description, ocurred_at) VALUES (?, ?, ?, ?, ?)")
	if err != nil {
		echo.Echo(echo.RedFG, "Error preparing insert statement: ")
		echo.EchoErr(err)
		return err
	}

	_, err = stmt.ExecContext(ctx, event.ID, event.Type, event.Actor, event.Description, event.OcurredAt)
	if err != nil {
		echo.Echo(echo.RedFG, "Error executing insert statement: ")
		echo.EchoErr(err)
		return err
	}

	return nil
}

func (sqlite *EventsSqliteDB) FindAllEvents(ctx context.Context) ([]*models.Event, error) {
	rows, err := sqlite.db.QueryContext(ctx, "SELECT id, type, actor, description, ocurred_at FROM events")
	if err != nil {
		echo.Echo(echo.RedFG, "Error querying all events: ")
		echo.EchoErr(err)
		return nil, err
	}

	var events []*models.Event
	for rows.Next() {
		var event models.Event
		err = rows.Scan(&event.ID, &event.Type, &event.Actor, &event.Description, &event.OcurredAt)
		if err != nil {
			echo.Echo(echo.RedFG, "Error scanning row: ")
			echo.EchoErr(err)
			return nil, err
		}

		events = append(events, &event)
	}

	return events, nil
}

func (sqlite *EventsSqliteDB) FindEventByID(ctx context.Context, event_id string) (*models.Event, error) {
	row := sqlite.db.QueryRowContext(ctx, "SELECT id, type, actor, description, ocurred_at FROM events WHERE id = ?", event_id)
	var event models.Event
	err := row.Scan(&event.ID, &event.Type, &event.Actor, &event.Description, &event.OcurredAt)
	if err != nil {
		echo.Echo(echo.RedFG, "Error on [FindEventByID] row: ")
		echo.EchoErr(err)
		return nil, err
	}

	return &event, nil
}

func (sqlite *EventsSqliteDB) FindEventsByType(ctx context.Context, event_type models.EventType) ([]*models.Event, error) {
	rows, err := sqlite.db.QueryContext(ctx, "SELECT id, type, actor, description, ocurred_at FROM events WHERE type = ?", string(event_type))
	if err != nil {
		echo.Echo(echo.RedFG, "Error querying all events on [FindEventsByType]: ")
		echo.EchoErr(err)
		return nil, err
	}

	var events []*models.Event
	for rows.Next() {
		var event models.Event
		err = rows.Scan(&event.ID, &event.Type, &event.Actor, &event.Description, &event.OcurredAt)
		if err != nil {
			echo.Echo(echo.RedFG, "Error scanning row on [FindEventsByType]: ")
			echo.EchoErr(err)
			return nil, err
		}

		events = append(events, &event)
	}

	return events, nil
}

func (sqlite *EventsSqliteDB) FindEventsByActor(ctx context.Context, actor string) ([]*models.Event, error) {
	rows, err := sqlite.db.QueryContext(ctx, "SELECT id, type, actor, description, ocurred_at FROM events WHERE actor = ?", actor)
	if err != nil {
		echo.Echo(echo.RedFG, "Error querying all events on [FindEventsByActor]: ")
		echo.EchoErr(err)
		return nil, err
	}

	var events []*models.Event
	for rows.Next() {
		var event models.Event
		err = rows.Scan(&event.ID, &event.Type, &event.Actor, &event.Description, &event.OcurredAt)
		if err != nil {
			echo.Echo(echo.RedFG, "Error scanning row on [FindEventsByActor]: ")
			echo.EchoErr(err)
			return nil, err
		}

		events = append(events, &event)
	}

	return events, nil
}

func (sqlite *EventsSqliteDB) Close() {
	sqlite.db.Close()
}
