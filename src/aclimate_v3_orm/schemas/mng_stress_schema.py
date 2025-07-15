from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from ..enums import StressCategory

class StressBase(BaseModel):
    name: str = Field(..., max_length=255)
    short_name: str = Field(..., max_length=100)
    category: StressCategory
    description: Optional[str] = None
    enable: bool = Field(default=True, description="Habilitado")

class StressCreate(StressBase):
    pass

class StressUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    short_name: Optional[str] = Field(None, max_length=100)
    category: Optional[StressCategory] = None
    description: Optional[str] = None

class StressRead(StressBase):
    id: int
    model_config = ConfigDict(from_attributes=True)