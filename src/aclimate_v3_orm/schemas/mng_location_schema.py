from typing import Optional
from .mng_admin_1_schema import Admin1Read
from .mng_admin_2_schema import Admin2Read
from .mng_country_schema import CountryRead
from .mng_source_schema import SourceRead
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

class LocationBase(BaseModel):
    """Base fields for locations"""
    admin_2_id: int = Field(..., gt=0, description="ID of the parent Admin2 region")
    source_id: int = Field(..., gt=0, description="ID of the associated source")
    name: str = Field(..., max_length=255, description="Name of the location")
    ext_id: str = Field(..., max_length=255, description="External ID/reference")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    altitude: float = Field(..., description="Altitude in meters")
    visible: bool = Field(default=True, description="Visibility status")
    enable: bool = Field(default=True, description="Active status")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is not empty"""
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

class LocationCreate(BaseModel):
    """Schema for creating new locations"""
    admin_2_id: int = Field(..., gt=0)
    source_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=255)
    ext_id: str = Field(..., max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: float = Field(...)
    visible: bool = Field(default=True)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is not empty"""
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

class LocationUpdate(BaseModel):
    """Schema for updating locations (all fields optional)"""
    admin_2_id: Optional[int] = Field(None, gt=0)
    source_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    ext_id: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    altitude: Optional[float] = None
    visible: Optional[bool] = None
    enable: Optional[bool] = None

    @field_validator('name', mode='before')
    @classmethod
    def validate_name_update(cls, v: Optional[str]) -> Optional[str]:
        """Handle empty values for optional name field"""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty")
            return v
        return None

class LocationRead(LocationBase):
    """Full location schema with read-only fields"""
    id: int
    admin_1: Optional[Admin1Read] = None
    admin_2: Optional[Admin2Read] = None
    country: Optional[CountryRead] = None
    source: Optional[SourceRead] = None
    
    model_config = ConfigDict(from_attributes=True)