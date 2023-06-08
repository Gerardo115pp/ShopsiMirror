package models

import (
	"time"

	"github.com/golang-jwt/jwt"
)

type AppClaims struct {
	ServiceID   string `json:"user_id"`
	ServiceName string `json:"service_name"`
	Role        string `json:"role"`
	Origin      string `json:"origin"`
	jwt.StandardClaims
}

func CreateToken(jwt_secret string, service BonhartService) (string, error) {
	claims := AppClaims{
		ServiceID:   service.ID,
		ServiceName: service.Name,
		Role:        service.Role,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(2 * (time.Hour * 24)).Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(jwt_secret))
}
