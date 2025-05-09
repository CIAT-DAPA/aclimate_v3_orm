from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class Admin2Base(BaseModel):
    """Base fields for administrative level 2 regions"""
    admin_1_id: int = Field(..., gt=0, description="ID of the parent Admin1 region")
    name: str = Field(..., max_length=255, description="Name of the administrative region")
    visible: bool = Field(default=True, description="Whether the region is visible")
    enable: bool = Field(default=True, description="Whether the region is enabled")

class Admin2Create(Admin2Base):
    """Schema for creating new Admin2 regions"""
    pass

class Admin2Update(BaseModel):
    """Schema for updating Admin2 regions"""
    admin_1_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    visible: Optional[bool] = None
    enable: Optional[bool] = None

class Admin2Read(Admin2Base):
    """Complete Admin2 schema including read-only fields and relationships"""
    id: int
    register: datetime
    updated: datetime
    
    # Relationships (uncomment if needed in responses)
    # admin_1: Optional['Admin1'] = None
    # locations: List['Location'] = []
    
    model_config = ConfigDict(from_attributes=True)  # Enable ORM compatibility