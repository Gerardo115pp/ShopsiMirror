package database

import (
	"bonhart_oauth_serivce/models"
	"context"
	"database/sql"
	"fmt"

	"github.com/Gerardo115pp/patriots_lib/echo"
	_ "github.com/mattn/go-sqlite3"
)

type SQLite3Repository struct {
	db *sql.DB
}

var local_oauth_cache map[string]*models.MeliOauthToken

func NewSQLite3Repository(filepath string) (*SQLite3Repository, error) {
	db, err := sql.Open("sqlite3", filepath)
	if err != nil {
		return nil, err
	}

	new_sqlite_storage := SQLite3Repository{db: db}
	new_sqlite_storage.loadTokens() // Load all tokens from database

	return &SQLite3Repository{db: db}, nil
}

func (sqlite *SQLite3Repository) InsertOauthToken(ctx context.Context, token *models.MeliOauthToken) error {
	if _, exists := local_oauth_cache[token.AppUser]; !exists {
		return fmt.Errorf("Shopsi User %s does not exists", token.UserID)
	}

	stmt, err := sqlite.db.Prepare("INSERT INTO meli_oauth_tokens(code, redirect_uri, client_id, client_secret, grant_type, access_token, token_type, expires_in, scope, refresh_token, user_id, app_user) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
	if err != nil {
		return err
	}

	_, err = stmt.ExecContext(ctx, token.Code, token.RedirectURI, token.ClientID, token.ClientSecret, token.GrantType, token.AccessToken, token.TokenType, token.ExpiresIn, token.Scope, token.RefreshToken, token.UserID, token.AppUser)
	if err != nil {
		return err
	}
	local_oauth_cache[token.AppUser] = token

	return nil
}

func (sqlite *SQLite3Repository) GetOauthTokenByAppUser(ctx context.Context, app_user string) (*models.MeliOauthToken, error) {
	var target_token *models.MeliOauthToken
	target_token, exists := local_oauth_cache[app_user]
	if !exists {
		return nil, fmt.Errorf("Shopsi User %s does not exists", app_user)
	}

	return target_token, nil
}

func (sqlite *SQLite3Repository) UpdateUserOauthToken(ctx context.Context, token *models.MeliOauthToken) error {
	if _, exists := local_oauth_cache[token.AppUser]; !exists {
		return fmt.Errorf("Shopsi User %s does not exists", token.UserID)
	}

	stmt, err := sqlite.db.Prepare("UPDATE meli_oauth_tokens SET code = ?, redirect_uri = ?, client_id = ?, client_secret = ?, grant_type = ?, access_token = ?, token_type = ?, expires_in = ?, scope = ?, refresh_token = ?, user_id = ? WHERE app_user = ?")
	if err != nil {
		return err
	}

	_, err = stmt.ExecContext(ctx, token.Code, token.RedirectURI, token.ClientID, token.ClientSecret, token.GrantType, token.AccessToken, token.TokenType, token.ExpiresIn, token.Scope, token.RefreshToken, token.UserID, token.AppUser)
	if err != nil {
		return err
	}

	local_oauth_cache[token.AppUser] = token

	return nil
}

func (sqlite *SQLite3Repository) loadTokens() {
	local_oauth_cache = make(map[string]*models.MeliOauthToken)

	rows, err := sqlite.db.Query("SELECT code, redirect_uri, client_id, client_secret, grant_type, access_token, token_type, expires_in, scope, refresh_token, user_id, app_user FROM meli_oauth_tokens")
	if err != nil {
		echo.EchoErr(err)
		return
	}

	var loaded_token *models.MeliOauthToken
	for rows.Next() {
		loaded_token = new(models.MeliOauthToken)

		err = rows.Scan(&loaded_token.Code, &loaded_token.RedirectURI, &loaded_token.ClientID, &loaded_token.ClientSecret, &loaded_token.GrantType, &loaded_token.AccessToken, &loaded_token.TokenType, &loaded_token.ExpiresIn, &loaded_token.Scope, &loaded_token.RefreshToken, &loaded_token.UserID, &loaded_token.AppUser)
		if err != nil {
			echo.EchoErr(err)
			continue
		}

		local_oauth_cache[loaded_token.AppUser] = loaded_token
	}
	echo.Echo(echo.GreenFG, "Loaded %d tokens from database", len(local_oauth_cache))
}

func (sqlite *SQLite3Repository) Close() error {
	return sqlite.db.Close()
}
