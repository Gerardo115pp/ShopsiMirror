package models

import (
	"github.com/golang-jwt/jwt"
)

type AppClaims struct {
	UserID   string `json:"user_id"`
	Username string `json:"username"`
	Email    string `json:"email"`
	jwt.StandardClaims
}
