package models

import (
	"math"
	"time"
)

type MeliOauthToken struct {
	Code         string `json:"code"`
	RedirectURI  string `json:"redirect_uri"`
	ClientID     string `json:"client_id"`
	ClientSecret string `json:"client_secret"`
	GrantType    string `json:"grant_type"`
	AccessToken  string `json:"access_token"`
	TokenType    string `json:"token_type"`
	ExpiresIn    int64  `json:"expires_in"`
	Scope        string `json:"scope"`
	UserID       string `json:"user_id"`
	RefreshToken string `json:"refresh_token"`
	AppUser      string `json:"app_user"`
}

func (oauth_token *MeliOauthToken) setTimeFormFloat(float_time float64) {
	seconds, mantissa := math.Modf(float_time)
	timestamp := time.Unix(int64(seconds), int64(mantissa*(1e9)))
	oauth_token.ExpiresIn = timestamp.Unix()
}

func (oauth_token *MeliOauthToken) setExpiresIn(new_timestamp int64) {
	oauth_token.ExpiresIn = time.Now().Add(time.Duration(new_timestamp) * time.Second).Unix()
}
