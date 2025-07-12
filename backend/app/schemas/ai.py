from pydantic import BaseModel
from typing import List, Optional
from app.models.obligation import PriorityEnum, CategoryEnum

class ExtractionRequest(BaseModel):
    text: str
    document_title: Optional[str] = None
    document_type: Optional[str] = None  # regulation, rfp, contract, etc.

class ExtractedObligation(BaseModel):
    obligation_text: str
    category: CategoryEnum
    priority: Optional[PriorityEnum] = None
    source_section: Optional[str] = None
    confidence_score: Optional[int] = None

class ExtractionResponse(BaseModel):
    obligations: List[ExtractedObligation]
    total_extracted: int
    processing_time: float

class SummarizationRequest(BaseModel):
    text: str
    max_length: Optional[int] = 500

class SummarizationResponse(BaseModel):
    summary: str
    key_points: List[str]
    processing_time: float

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    category_filter: Optional[CategoryEnum] = None
    priority_filter: Optional[PriorityEnum] = None

class SearchResult(BaseModel):
    obligation_id: int
    text: str
    category: CategoryEnum
    priority: Optional[PriorityEnum]
    source_section: Optional[str]
    document_title: str
    similarity_score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    processing_time: float 