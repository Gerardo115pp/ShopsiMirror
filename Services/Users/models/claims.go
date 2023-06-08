package models

import (
	"time"

	"github.com/golang-jwt/jwt"
)

type AppClaims struct {
	UserID   string `json:"user_id"`
	Username string `json:"username"`
	Email    string `json:"email"`
	jwt.StandardClaims
}

func CreateToken(user *ShopsiUser, jwt_secret string) (string, error) {
	claims := AppClaims{
		UserID:   user.ID,
		Username: user.Username,
		Email:    user.Email,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(2 * (time.Hour * 24)).Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(jwt_secret))
}
