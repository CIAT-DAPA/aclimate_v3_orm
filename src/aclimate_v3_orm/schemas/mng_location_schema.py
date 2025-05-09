from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

class LocationBase(BaseModel):
    """Base fields for locations"""
    admin_2_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=255)
    ext_id: Optional[str] = Field(None, max_length=255)
    origin: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    altitude: Optional[float] = None
    visible: bool = Field(default=True)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is not empty"""
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

class LocationCreate(LocationBase):
    """Schema for creating new locations (input validation only)"""
    pass

class LocationUpdate(BaseModel):
    """Schema for updating locations (all fields optional)"""
    admin_2_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    ext_id: Optional[str] = Field(None, max_length=255)
    origin: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    altitude: Optional[float] = None
    visible: Optional[bool] = None
    enable: Optional[bool] = None

class LocationRead(LocationBase):
    """Full location schema with read-only fields (ORM compatible)"""
    id: int
    enable: bool
    register: datetime
    updated: datetime
    
    model_config = ConfigDict(from_attributes=True)  # ORM compatibility