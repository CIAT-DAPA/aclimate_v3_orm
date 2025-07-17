from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ConfigurationFileBase(BaseModel):
    setup_id: int = Field(..., gt=0, description="ID del setup")
    name: str = Field(..., max_length=255, description="Nombre del archivo")
    path: str = Field(..., max_length=255, description="Ruta del archivo")
    enable: bool = Field(default=True, description="Habilitado")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class ConfigurationFileCreate(BaseModel):
    setup_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=255)
    path: str = Field(..., max_length=255)
    enable: bool = Field(default=True)

class ConfigurationFileUpdate(BaseModel):
    setup_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, max_length=255)
    path: Optional[str] = Field(None, max_length=255)
    enable: Optional[bool] = None

class ConfigurationFileRead(ConfigurationFileBase):
    id: int
    model_config = ConfigDict(from_attributes=True)