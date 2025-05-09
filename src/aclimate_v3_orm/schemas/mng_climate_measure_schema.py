from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ClimateMeasureBase(BaseModel):
    """Base fields for climate measures"""
    name: str = Field(..., max_length=150)
    short_name: str = Field(..., max_length=75)
    unit: str = Field(..., max_length=50)
    description: Optional[str] = None
    enable: bool = Field(default=True)

    @field_validator('name', 'short_name')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Ensure field is not empty or whitespace"""
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty")
        return v

class ClimateMeasureCreate(ClimateMeasureBase):
    """Schema for creating new measures (input validation only)"""
    pass

class ClimateMeasureUpdate(BaseModel):
    """Schema for updating measures (all fields optional)"""
    name: Optional[str] = Field(None, max_length=150)
    short_name: Optional[str] = Field(None, max_length=75)
    unit: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    enable: Optional[bool] = None

    @field_validator('name', 'short_name', mode='before')
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        """Handle empty values for optional fields"""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty")
            return v
        return None

class ClimateMeasureRead(ClimateMeasureBase):
    """Full measure schema with read-only fields (ORM compatible)"""
    id: int
    register: datetime
    updated: datetime
    
    model_config = ConfigDict(from_attributes=True)  # ORM compatibility