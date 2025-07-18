from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.models.obligation import PriorityEnum, CategoryEnum

class ExtractionRequest(BaseModel):
    text: str
    document_title: Optional[str] = None
    document_type: Optional[str] = None  # regulation, rfp, contract, etc.
    business_context: Optional[str] = None  # Enterprise context for better extraction
    compliance_frameworks: Optional[List[str]] = None  # Relevant frameworks to consider

class ExtractedObligation(BaseModel):
    obligation_text: str
    category: CategoryEnum
    priority: Optional[PriorityEnum] = None
    source_section: Optional[str] = None
    confidence_score: Optional[int] = None
    business_impact: Optional[str] = None  # Description of business impact
    compliance_framework: Optional[str] = None  # Relevant compliance framework
    risk_level: Optional[str] = None  # Risk assessment
    estimated_effort: Optional[str] = None  # Implementation effort estimate

class ExtractionResponse(BaseModel):
    obligations: List[ExtractedObligation]
    total_extracted: int
    processing_time: float
    document_metadata: Optional[Dict[str, Any]] = None  # Document structure analysis

class SummarizationRequest(BaseModel):
    text: str
    max_length: Optional[int] = 500
    include_requirements: Optional[bool] = True  # Focus on requirements/obligations
    include_risks: Optional[bool] = True  # Include risk assessment

class SummarizationResponse(BaseModel):
    summary: str
    key_points: List[str]
    processing_time: float
    requirements_summary: Optional[str] = None  # Summary focused on requirements
    risk_assessment: Optional[str] = None  # Risk summary

class DocumentStructureRequest(BaseModel):
    text: str
    document_type: Optional[str] = "general"
    include_metadata: Optional[bool] = True

class DocumentStructureResponse(BaseModel):
    document_type: str
    key_sections: List[str]
    stakeholders: List[str]
    compliance_areas: List[str]
    risk_level: str
    action_items_count: int
    deadlines: List[str]
    summary: str
    processing_time: float

class ComplianceMappingRequest(BaseModel):
    obligation_text: str
    existing_controls: List[str]
    compliance_frameworks: Optional[List[str]] = None

class ComplianceMappingResponse(BaseModel):
    suggested_mappings: List[Dict[str, Any]]
    gap_analysis: List[Dict[str, Any]]
    compliance_frameworks: List[str]
    processing_time: float

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    category_filter: Optional[CategoryEnum] = None
    priority_filter: Optional[PriorityEnum] = None
    compliance_framework_filter: Optional[str] = None  # Filter by compliance framework
    risk_level_filter: Optional[str] = None  # Filter by risk level

class SearchResult(BaseModel):
    obligation_id: int
    text: str
    category: CategoryEnum
    priority: Optional[PriorityEnum]
    source_section: Optional[str]
    document_title: str
    similarity_score: float
    business_impact: Optional[str] = None
    compliance_framework: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    processing_time: float

class GapAnalysisRequest(BaseModel):
    obligations: List[int]  # Obligation IDs to analyze
    target_frameworks: Optional[List[str]] = None  # Target compliance frameworks
    include_controls: Optional[bool] = True  # Include existing controls in analysis

class GapAnalysisResponse(BaseModel):
    unmapped_obligations: List[Dict[str, Any]]
    compliance_gaps: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    processing_time: float 