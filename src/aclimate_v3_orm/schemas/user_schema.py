from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from .role_schema import RoleRead
from datetime import datetime

class UserBase(BaseModel):
    keycloak_ext_id: str = Field(..., max_length=255, description="External Keycloak ID")
    role_id: int = Field(..., gt=0, description="Role ID")
    enable: bool = Field(default=True, description="Whether the user is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

    @field_validator('keycloak_ext_id')
    @classmethod
    def validate_keycloak_ext_id(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Keycloak external ID cannot be empty")
        return v

class UserCreate(BaseModel):
    keycloak_ext_id: str = Field(..., max_length=255, description="External Keycloak ID")
    role_id: int = Field(..., gt=0, description="Role ID")
    enable: bool = Field(default=True, description="Whether the user is enabled")

    @field_validator('keycloak_ext_id')
    @classmethod
    def validate_keycloak_ext_id(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Keycloak external ID cannot be empty")
        return v

class UserUpdate(BaseModel):
    keycloak_ext_id: Optional[str] = Field(None, max_length=255)
    role_id: Optional[int] = Field(None, gt=0)
    enable: Optional[bool] = None

    @field_validator('keycloak_ext_id', mode='before')
    @classmethod
    def validate_keycloak_ext_id_update(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Keycloak external ID cannot be empty")
            return v
        return None

class UserRead(UserBase):
    id: int
    role: Optional[RoleRead] = None
    model_config = ConfigDict(from_attributes=True)
    
    