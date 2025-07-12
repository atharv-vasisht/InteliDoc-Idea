from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.mapping import MappingTypeEnum

class MappingBase(BaseModel):
    obligation_id: int
    mapping_type: MappingTypeEnum
    external_id: str
    external_name: str
    external_url: Optional[str] = None
    notes: Optional[str] = None

class MappingCreate(MappingBase):
    mapped_by: int

class MappingUpdate(BaseModel):
    mapping_type: Optional[MappingTypeEnum] = None
    external_id: Optional[str] = None
    external_name: Optional[str] = None
    external_url: Optional[str] = None
    notes: Optional[str] = None

class MappingInDB(MappingBase):
    id: int
    mapped_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Mapping(MappingInDB):
    pass 