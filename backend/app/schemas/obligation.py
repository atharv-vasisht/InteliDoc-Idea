from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.obligation import PriorityEnum, CategoryEnum

class ObligationBase(BaseModel):
    text: str
    category: CategoryEnum
    priority: Optional[PriorityEnum] = None
    source_section: Optional[str] = None
    confidence_score: Optional[int] = None

class ObligationCreate(ObligationBase):
    document_id: int
    extracted_by: int

class ObligationUpdate(BaseModel):
    text: Optional[str] = None
    category: Optional[CategoryEnum] = None
    priority: Optional[PriorityEnum] = None
    source_section: Optional[str] = None
    confidence_score: Optional[int] = None

class ObligationInDB(ObligationBase):
    id: int
    document_id: int
    extracted_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Obligation(ObligationInDB):
    pass

class ObligationWithMappings(Obligation):
    mappings: List["Mapping"] = []

    class Config:
        from_attributes = True 