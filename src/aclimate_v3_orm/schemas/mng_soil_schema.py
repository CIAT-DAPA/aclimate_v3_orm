from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .mng_country_schema import CountryRead
from .mng_crop_schema import CropRead

class SoilBase(BaseModel):
    """Base fields for soil records"""
    country_id: int = Field(..., gt=0, description="ID of the associated country")
    crop_id: int = Field(..., gt=0, description="ID of the associated crop")
    name: str = Field(..., max_length=255, description="Name of the soil type")
    sort_order: int = Field(..., ge=0, description="Sort order for the soil type")
    enable: bool = Field(default=True, description="Whether the soil type is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class SoilCreate(BaseModel):
    """Schema for creating new soil records"""
    country_id: int = Field(..., gt=0, description="ID of the associated country")
    crop_id: int = Field(..., gt=0, description="ID of the associated crop")
    name: str = Field(..., max_length=255, description="Name of the soil type")
    sort_order: int = Field(..., ge=0, description="Sort order for the soil type")
    enable: bool = Field(default=True, description="Whether the soil type is enabled")

class SoilUpdate(BaseModel):
    """Schema for updating soil records"""
    country_id: Optional[int] = Field(None, gt=0)
    crop_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    sort_order: Optional[int] = Field(None, ge=0)
    enable: Optional[bool] = None

class SoilRead(SoilBase):
    """Complete soil schema including read-only fields"""
    id: int
    country: Optional[CountryRead] = None
    crop: Optional[CropRead] = None
    model_config = ConfigDict(from_attributes=True)