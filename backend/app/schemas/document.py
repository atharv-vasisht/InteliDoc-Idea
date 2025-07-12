from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    filename: str
    file_path: str
    file_size: int
    file_type: str

class DocumentCreate(DocumentBase):
    uploaded_by: int

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None

class DocumentInDB(DocumentBase):
    id: int
    content: Optional[str] = None
    summary: Optional[str] = None
    uploaded_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Document(DocumentInDB):
    pass 