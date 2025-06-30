from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CropBase(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre del cultivo")
    enable: bool = Field(default=True, description="Habilitado")
    register: Optional[datetime] = Field(None, description="Fecha de registro")
    updated: Optional[datetime] = Field(None, description="Fecha de actualización")

class CropCreate(BaseModel):
    name: str = Field(..., max_length=255)
    enable: bool = Field(default=True)

class CropUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    enable: Optional[bool] = None

class CropRead(CropBase):
    id: int
    model_config = ConfigDict(from_attributes=True)