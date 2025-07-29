from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CropBase(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre del cultivo")
    enable: bool = Field(default=True, description="Habilitado")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class CropCreate(BaseModel):
    name: str = Field(..., max_length=255)
    enable: bool = Field(default=True)

class CropUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    enable: Optional[bool] = None

class CropRead(CropBase):
    id: int
    model_config = ConfigDict(from_attributes=True)