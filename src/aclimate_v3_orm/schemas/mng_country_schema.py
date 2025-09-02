from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class CountryBase(BaseModel):
    """Base fields for countries"""
    name: str = Field(..., max_length=255, description="Full country name")
    iso2: str = Field(..., min_length=2, max_length=2, description="2-letter ISO country code")
    enable: bool = Field(default=True, description="Whether the country is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

    @field_validator('iso2')
    @classmethod
    def validate_iso2(cls, v: str) -> str:
        """Validate ISO2 code is uppercase"""
        if not v.isalpha() or not v.isupper():
            raise ValueError("ISO2 code must be 2 uppercase letters")
        return v

class CountryCreate(BaseModel):
    """Schema for creating new countries"""
    name: str = Field(..., max_length=255, description="Full country name")
    iso2: str = Field(..., min_length=2, max_length=2, description="2-letter ISO country code")
    enable: bool = Field(default=True, description="Whether the country is enabled")

    @field_validator('iso2')
    @classmethod
    def validate_iso2(cls, v: str) -> str:
        """Validate ISO2 code is uppercase"""
        if not v.isalpha() or not v.isupper():
            raise ValueError("ISO2 code must be 2 uppercase letters")
        return v

class CountryUpdate(BaseModel):
    """Schema for updating countries"""
    name: Optional[str] = Field(None, max_length=255)
    iso2: Optional[str] = Field(None, min_length=2, max_length=2)
    enable: Optional[bool] = None

    @field_validator('iso2', mode='before')
    @classmethod
    def validate_iso2_update(cls, v: Optional[str]) -> Optional[str]:
        """Validate ISO2 code if provided"""
        if v is not None:
            if not v.isalpha() or not v.isupper():
                raise ValueError("ISO2 code must be 2 uppercase letters")
        return v

class CountryRead(CountryBase):
    """Complete country schema including read-only fields"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)