from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from ..enums import Apps

class RoleBase(BaseModel):
    name: str = Field(..., max_length=255, description="Role name")
    app: Apps = Field(..., description="Application enum")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Role name cannot be empty")
        return v

class RoleCreate(BaseModel):
    name: str = Field(..., max_length=255, description="Role name")
    app: Apps = Field(..., description="Application enum")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Role name cannot be empty")
        return v

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    app: Optional[Apps] = None

    @field_validator('name', mode='before')
    @classmethod
    def validate_name_update(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Role name cannot be empty")
            return v
        return None

class RoleRead(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
