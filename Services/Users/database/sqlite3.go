package database

import (
	"context"
	"database/sql"
	"fmt"
	"shopsi_users_service/models"

	"github.com/Gerardo115pp/patriots_lib/echo"
	_ "github.com/mattn/go-sqlite3"
)

type SQLite3Repository struct {
	db *sql.DB
}

var local_shopsi_cache map[string]*models.ShopsiUser

func NewSQLite3Repository(filepath string) (*SQLite3Repository, error) {
	db, err := sql.Open("sqlite3", filepath)
	if err != nil {
		return nil, err
	}

	new_sqlite_storage := SQLite3Repository{db: db}
	new_sqlite_storage.loadShopsiUsers() // Load all customers from database

	return &SQLite3Repository{db: db}, nil
}

func (sqlite *SQLite3Repository) InsertShopsiUser(ctx context.Context, customer *models.ShopsiUser) error {
	if _, exists := local_shopsi_cache[customer.ID]; exists {
		return fmt.Errorf("Shopsi User %s already exists", customer.ID)
	}

	stmt, err := sqlite.db.Prepare("INSERT INTO shopsi_users(id, username, email, password) VALUES(?, ?, ?, ?)")
	if err != nil {
		return err
	}

	_, err = stmt.ExecContext(ctx, customer.ID, customer.Username, customer.Email, customer.Password)
	if err != nil {
		return err
	}

	local_shopsi_cache[customer.ID] = customer
	return nil
}

func (sqlite *SQLite3Repository) GetShopsiUserByID(ctx context.Context, id string) (*models.ShopsiUser, error) {
	var target_customer *models.ShopsiUser = new(models.ShopsiUser)
	var err error

	if target_customer, exists := local_shopsi_cache[id]; exists {
		return target_customer, nil
	}

	echo.EchoWarn(fmt.Sprintf("Customer %s not found in cache", id))

	err = sqlite.db.QueryRow("SELECT id, username, email, password FROM shopsi_users WHERE id = ?", id).Scan(&target_customer.ID, &target_customer.Username, &target_customer.Email, &target_customer.Password)
	return target_customer, err
}

func (sqlite *SQLite3Repository) GetShopsiUserByEmail(ctx context.Context, email string) (*models.ShopsiUser, error) {
	var target_customer *models.ShopsiUser = new(models.ShopsiUser)
	var err error

	err = sqlite.db.QueryRow("SELECT id, username, email, password FROM shopsi_users WHERE email = ?", email).Scan(&target_customer.ID, &target_customer.Username, &target_customer.Email, &target_customer.Password)
	if err != nil {
		return nil, err
	}
	return target_customer, err
}

func (sqlite *SQLite3Repository) GetShopsiUserByUsername(ctx context.Context, username string) (*models.ShopsiUser, error) {
	var target_customer *models.ShopsiUser = new(models.ShopsiUser)
	var err error

	err = sqlite.db.QueryRow("SELECT id, username, email, password FROM shopsi_users WHERE username = ?", username).Scan(&target_customer.ID, &target_customer.Username, &target_customer.Email, &target_customer.Password)
	if err != nil {
		return nil, err
	}
	return target_customer, err
}

func (sqlite *SQLite3Repository) GetAllShopsiUsers(ctx context.Context) ([]*models.ShopsiUser, error) {
	var customers []*models.ShopsiUser = make([]*models.ShopsiUser, 0)

	rows, err := sqlite.db.Query("SELECT id, username, email, password FROM shopsi_users")
	if err != nil {
		return nil, err
	}

	for rows.Next() {
		var customer *models.ShopsiUser = new(models.ShopsiUser)
		err = rows.Scan(&customer.ID, &customer.Username, &customer.Email, &customer.Password)
		if err != nil {
			return nil, err
		}
		customers = append(customers, customer)
	}

	return customers, nil
}

func (sqlite *SQLite3Repository) UserExists(ctx context.Context, user *models.ShopsiUser) bool {
	var sql_query string = "SELECT * FROM shopsi_users WHERE username = ? OR email = ?"
	stmt, err := sqlite.db.Prepare(sql_query)

	rows, err := stmt.QueryContext(ctx, user.Username, user.Email)
	if err != nil {
		return false
	}

	return rows.Next()
}

func (sqlite *SQLite3Repository) UpdateShopsiUser(ctx context.Context, customer *models.ShopsiUser) error {
	if _, exists := local_shopsi_cache[customer.ID]; !exists {
		return fmt.Errorf("Shopsi User %s does not exists", customer.ID)
	}

	stmt, err := sqlite.db.Prepare("UPDATE shopsi_users SET username = ?, email = ?, password = ? WHERE id = ?")
	if err != nil {
		return err
	}

	_, err = stmt.ExecContext(ctx, customer.Username, customer.Email, customer.Password, customer.ID)
	if err != nil {
		return err
	}

	local_shopsi_cache[customer.ID] = customer
	return nil
}

func (sqlite *SQLite3Repository) loadShopsiUsers() error {
	if local_shopsi_cache != nil {
		echo.EchoErr(fmt.Errorf("Orders already loaded"))
	}

	local_shopsi_cache = make(map[string]*models.ShopsiUser)

	rows, err := sqlite.db.Query("SELECT id, username, email, password FROM shopsi_users")
	if err != nil {
		return err
	}

	for rows.Next() {
		var customer *models.ShopsiUser = new(models.ShopsiUser)
		err = rows.Scan(&customer.ID, &customer.Username, &customer.Email, &customer.Password)
		if err != nil {
			return err
		}
		echo.EchoDebug(fmt.Sprintf("Loaded customer %s", customer.Username))
		local_shopsi_cache[customer.ID] = customer
	}

	return nil
}

func (sqlite *SQLite3Repository) DeleteShopsiUser(ctx context.Context, username string, email string) error {
	stmt, err := sqlite.db.Prepare("DELETE FROM shopsi_users WHERE username = ? AND email = ?")
	if err != nil {
		return err
	}

	_, err = stmt.ExecContext(ctx, username, email)
	if err != nil {
		return err
	}

	for id, customer := range local_shopsi_cache {
		if customer.Username == username && customer.Email == email {
			delete(local_shopsi_cache, id)
		}
	}

	return nil
}

func (sqlite *SQLite3Repository) Close() error {
	return sqlite.db.Close()
}
