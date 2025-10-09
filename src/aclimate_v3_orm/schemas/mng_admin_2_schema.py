from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from .mng_admin_1_schema import Admin1Read
from .mng_country_schema import CountryRead

class Admin2Base(BaseModel):
    """Base fields for administrative level 2 regions"""
    admin_1_id: int = Field(..., gt=0, description="ID of the parent Admin1 region")
    name: str = Field(..., max_length=255, description="Name of the administrative region")
    ext_id: str = Field(default="", max_length=255, description="External identifier")
    visible: bool = Field(default=True, description="Whether the region is visible")
    enable: bool = Field(default=True, description="Whether the region is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class Admin2Create(BaseModel):
    """Schema for creating new Admin2 regions"""
    admin_1_id: int = Field(..., gt=0, description="ID of the parent Admin1 region")
    name: str = Field(..., max_length=255, description="Name of the administrative region")
    ext_id: str = Field(default="", max_length=255, description="External identifier")
    visible: bool = Field(default=True, description="Whether the region is visible")
    enable: bool = Field(default=True, description="Whether the region is enabled")

class Admin2Update(BaseModel):
    """Schema for updating Admin2 regions"""
    admin_1_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    ext_id: Optional[str] = Field(None, max_length=255)
    visible: Optional[bool] = None
    enable: Optional[bool] = None

class Admin2Read(Admin2Base):
    """Complete Admin2 schema including read-only fields and relationships"""
    id: int
    
    admin_1: Optional[Admin1Read] = None
    country: Optional[CountryRead] = None
    
    model_config = ConfigDict(from_attributes=True)