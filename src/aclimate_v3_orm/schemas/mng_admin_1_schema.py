from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class Admin1Base(BaseModel):
    """Base fields for administrative level 1 regions"""
    country_id: int = Field(..., gt=0, description="ID of the associated country")
    name: str = Field(..., max_length=255, description="Name of the administrative region")
    enable: bool = Field(default=True, description="Whether the region is enabled")

class Admin1Create(Admin1Base):
    """Schema for creating new Admin1 regions"""
    pass

class Admin1Update(BaseModel):
    """Schema for updating Admin1 regions"""
    country_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    enable: Optional[bool] = None

class Admin1Read(Admin1Base):
    """Complete Admin1 schema including read-only fields"""
    id: int
    register: datetime
    updated: datetime
    
    model_config = ConfigDict(from_attributes=True)  # Enable ORM compatibility
    
