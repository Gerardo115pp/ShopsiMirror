package models

import (
	"fmt"

	"github.com/google/uuid"
)

type BonhartService struct {
	ID     string `json:"id"`
	Name   string `json:"name"`
	Role   string `json:"role"`
	Origin string `json:"origin"`
}

func CreateBonhartServiceObject(name string, role string, origin string) *BonhartService {
	var service *BonhartService = new(BonhartService)
	service.ID = fmt.Sprintf("bonhart-service-%s", uuid.New().String())
	service.Name = name
	service.Role = role
	service.Origin = origin
	return service
}
