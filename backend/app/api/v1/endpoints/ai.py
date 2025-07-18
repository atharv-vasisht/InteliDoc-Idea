from fastapi import APIRouter, HTTPException, Depends, Body, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import time
import os
import json

from app.core.database import get_async_db
from app.services.ai_service import ai_service
from app.schemas.ai import (
    ExtractionRequest, 
    ExtractionResponse, 
    SummarizationRequest, 
    SummarizationResponse,
    DocumentStructureRequest,
    DocumentStructureResponse,
    ComplianceMappingRequest,
    ComplianceMappingResponse,
    GapAnalysisRequest,
    GapAnalysisResponse
)

router = APIRouter()

@router.post("/extract-obligations", response_model=ExtractionResponse)
async def extract_obligations(
    request: ExtractionRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Extract obligations/requirements from text using AI
    """
    start_time = time.time()
    
    try:
        # Extract obligations using AI service
        extracted_obligations = ai_service.extract_obligations(request)
        
        processing_time = time.time() - start_time
        
        return ExtractionResponse(
            obligations=extracted_obligations,
            total_extracted=len(extracted_obligations),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting obligations: {str(e)}"
        )

@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_text(
    request: SummarizationRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Generate a summary of the provided text
    """
    try:
        # Generate summary using AI service
        result = ai_service.summarize_text(request)
        
        return SummarizationResponse(
            summary=result["summary"],
            key_points=result["key_points"],
            processing_time=result["processing_time"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summary: {str(e)}"
        ) 

@router.post("/propose-reorg")
async def propose_reorg(folder_path: str = "test_documents"):
    """Analyze folder and propose reorganization plan using AI"""
    result = ai_service.analyze_and_propose_reorg(folder_path)
    return result 

@router.post("/chat-reorg")
async def chat_reorg(
    message: str = Body(..., embed=True),
    folder_path: str = "test_documents"
):
    """Chat-driven AI reorg: user command + folder context -> AI diff"""
    folder_tree = {}
    file_summaries = {}
    for root, dirs, files in os.walk(folder_path):
        rel_root = os.path.relpath(root, folder_path)
        folder_tree[rel_root] = files
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(2000)
            except Exception as e:
                content = f"[Error reading file: {e}]"
            summary_prompt = f"Summarize the following file for project management, compliance, and PMO context.\n\nFILENAME: {file}\nCONTENT:\n{content}\n\nReturn a 1-2 sentence summary."
            try:
                model = ai_service.model
                gen_model = ai_service.model
                model = ai_service.model
                response = ai_service.model.generate_content(summary_prompt)
                summary = response.text.strip()
            except Exception as e:
                summary = f"[AI summary error: {e}]"
            file_summaries[file_path] = summary
    chat_prompt = (
        "You are an expert in project management and compliance document organization. "
        "Given the following folder structure and file summaries, and the following user command, propose a JSON diff of changes to apply. "
        "Do not include markdown or code blocks.\n\n"
        f"FOLDER TREE: {folder_tree}\n\nFILE SUMMARIES: {file_summaries}\n\nUSER COMMAND: {message}\n\n"
        "Return a JSON array of changes, where each change is an object with 'action' (move, rename, create), 'source', 'destination', and 'details' fields as needed."
    )
    try:
        model = ai_service.model
        gen_model = ai_service.model
        model = ai_service.model
        response = ai_service.model.generate_content(chat_prompt)
        plan = response.text.strip()
        try:
            plan_json = json.loads(plan)
        except Exception as e:
            print(f"JSON parsing error in chat-reorg plan: {e}\nRaw response: {plan}")
            plan_json = plan
        return {
            "folder_tree": folder_tree,
            "file_summaries": file_summaries,
            "user_message": message,
            "proposed_changes": plan_json
        }
    except Exception as e:
        print(f"Gemini API error in chat-reorg: {e}")
        return {"error": str(e)} 

@router.post("/upload-folder")
async def upload_folder(files: List[UploadFile] = File(...), relative_paths: List[str] = Form(...)):
    """Accept multiple files with relative paths for folder upload."""
    # For MVP, just log the file names and paths
    file_info = [{"filename": f.filename, "relative_path": p} for f, p in zip(files, relative_paths)]
    print("Received folder upload:", file_info)
    return {"status": "success", "files": file_info}

@router.post("/analyze-document-structure", response_model=DocumentStructureResponse)
async def analyze_document_structure(
    request: DocumentStructureRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Analyze document structure and extract metadata for enterprise document management
    """
    start_time = time.time()
    
    try:
        result = ai_service.analyze_document_structure(request.text, request.document_type)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return DocumentStructureResponse(
            document_type=result.get("document_type", "general"),
            key_sections=result.get("key_sections", []),
            stakeholders=result.get("stakeholders", []),
            compliance_areas=result.get("compliance_areas", []),
            risk_level=result.get("risk_level", "medium"),
            action_items_count=result.get("action_items_count", 0),
            deadlines=result.get("deadlines", []),
            summary=result.get("summary", ""),
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document analysis failed: {str(e)}")

@router.post("/compliance-mapping", response_model=ComplianceMappingResponse)
async def generate_compliance_mapping(
    request: ComplianceMappingRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Generate compliance mapping suggestions for obligations
    """
    start_time = time.time()
    
    try:
        result = ai_service.generate_compliance_mapping(
            request.obligation_text, 
            request.existing_controls
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return ComplianceMappingResponse(
            suggested_mappings=result.get("suggested_mappings", []),
            gap_analysis=result.get("gap_analysis", []),
            compliance_frameworks=result.get("compliance_frameworks", []),
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance mapping failed: {str(e)}")

@router.post("/gap-analysis", response_model=GapAnalysisResponse)
async def perform_gap_analysis(
    request: GapAnalysisRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Perform comprehensive gap analysis for compliance and requirements
    """
    start_time = time.time()
    
    try:
        # This would integrate with your existing obligations and mappings
        # For now, return a placeholder response
        return GapAnalysisResponse(
            unmapped_obligations=[],
            compliance_gaps=[],
            risk_assessment={
                "overall_risk": "medium",
                "high_risk_items": 0,
                "medium_risk_items": 0,
                "low_risk_items": 0
            },
            recommendations=[
                "Implement missing controls for high-priority obligations",
                "Review and update existing mappings",
                "Establish monitoring for compliance gaps"
            ],
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gap analysis failed: {str(e)}") 