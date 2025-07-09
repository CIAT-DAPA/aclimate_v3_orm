from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from ..enums import SourceType

class SourceBase(BaseModel):
    """Base fields for management sources"""
    name: str = Field(..., max_length=255, description="Source name")
    source_type: SourceType = Field(..., description="Type of source: MA (Manual) or AU (Automatic)")
    enable: bool = Field(default=True, description="Whether the source is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

    model_config = ConfigDict(use_enum_values=True)

class SourceCreate(BaseModel):
    """Schema for creating new management sources"""
    name: str = Field(..., max_length=255, description="Source name")
    source_type: SourceType = Field(..., description="Type of source: MA (Manual) or AU (Automatic)")
    enable: bool = Field(default=True, description="Whether the source is enabled")

class SourceUpdate(BaseModel):
    """Schema for updating management sources"""
    name: Optional[str] = Field(None, max_length=255)
    source_type: Optional[SourceType] = None
    enable: Optional[bool] = None

class SourceRead(SourceBase):
    """Complete management source schema including read-only fields"""
    id: int
    
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )