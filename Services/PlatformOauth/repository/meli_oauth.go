package repository

import (
	"bonhart_oauth_serivce/models"
	"context"
)

type MeliOauth interface {
	InsertOauthToken(ctx context.Context, token *models.MeliOauthToken) error
	GetOauthTokenByAppUser(ctx context.Context, app_user string) (*models.MeliOauthToken, error)
	UpdateUserOauthToken(ctx context.Context, token *models.MeliOauthToken) error
	Close() error
}

var order_repo_implentation MeliOauth

func SetRepository(repository MeliOauth) {
	order_repo_implentation = repository
}

func InsertOauthToken(ctx context.Context, token *models.MeliOauthToken) error {
	return order_repo_implentation.InsertOauthToken(ctx, token)
}

func GetOauthTokenByAppUser(ctx context.Context, app_user string) (*models.MeliOauthToken, error) {
	return order_repo_implentation.GetOauthTokenByAppUser(ctx, app_user)
}

func UpdateUserOauthToken(ctx context.Context, token *models.MeliOauthToken) error {
	return order_repo_implentation.UpdateUserOauthToken(ctx, token)
}

func Close() error {
	return order_repo_implentation.Close()
}
