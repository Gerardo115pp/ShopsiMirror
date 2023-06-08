package repository

import (
	"context"
	"shopsi_users_service/models"
)

type CustomerRepository interface {
	InsertShopsiUser(ctx context.Context, order *models.ShopsiUser) error
	GetShopsiUserByID(ctx context.Context, id string) (*models.ShopsiUser, error)
	GetShopsiUserByEmail(ctx context.Context, email string) (*models.ShopsiUser, error)
	GetShopsiUserByUsername(ctx context.Context, username string) (*models.ShopsiUser, error)
	GetAllShopsiUsers(ctx context.Context) ([]*models.ShopsiUser, error)
	UserExists(ctx context.Context, user *models.ShopsiUser) bool
	DeleteShopsiUser(ctx context.Context, username string, email string) error
	UpdateShopsiUser(ctx context.Context, customer *models.ShopsiUser) error
	Close() error
}

var order_repo_implentation CustomerRepository

func SetShopsiUserRepository(repository CustomerRepository) {
	order_repo_implentation = repository
}

func InsertShopsiUser(ctx context.Context, order *models.ShopsiUser) error {
	return order_repo_implentation.InsertShopsiUser(ctx, order)
}

func GetShopsiUserByID(ctx context.Context, id string) (*models.ShopsiUser, error) {
	return order_repo_implentation.GetShopsiUserByID(ctx, id)
}

func GetShopsiUserByEmail(ctx context.Context, email string) (*models.ShopsiUser, error) {
	return order_repo_implentation.GetShopsiUserByEmail(ctx, email)
}

func GetShopsiUserByUsername(ctx context.Context, username string) (*models.ShopsiUser, error) {
	return order_repo_implentation.GetShopsiUserByUsername(ctx, username)
}

func GetAllShopsiUsers(ctx context.Context) ([]*models.ShopsiUser, error) {
	return order_repo_implentation.GetAllShopsiUsers(ctx)
}

func UserExists(ctx context.Context, user *models.ShopsiUser) bool {
	return order_repo_implentation.UserExists(ctx, user)
}

func DeleteShopsiUser(ctx context.Context, username string, email string) error {
	return order_repo_implentation.DeleteShopsiUser(ctx, username, email)
}

func UpdateShopsiUser(ctx context.Context, customer *models.ShopsiUser) error {
	return order_repo_implentation.UpdateShopsiUser(ctx, customer)
}

func Close() error {
	return order_repo_implentation.Close()
}
