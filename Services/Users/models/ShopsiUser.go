package models

import (
	"fmt"

	"github.com/Gerardo115pp/patriots_lib/echo"
	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

type ShopsiUser struct {
	ID       string `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

func HashUserPassword(password string) string {
	hashed_password, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		echo.EchoFatal(err)
	}
	return string(hashed_password)
}

func CreateShopsiUserObject(email string, password string, username string) *ShopsiUser {
	var customer *ShopsiUser = new(ShopsiUser)
	customer.ID = fmt.Sprintf("shopsi-user-%s", uuid.New().String())
	customer.Email = email
	customer.Username = username
	customer.Password = HashUserPassword(password)
	return customer
}
