from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class IndicatorCategoryBase(BaseModel):
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    enable: bool = Field(default=True, description="Whether the category is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class IndicatorCategoryCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    enable: bool = Field(default=True)

class IndicatorCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    enable: Optional[bool] = None

class IndicatorCategoryRead(IndicatorCategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
