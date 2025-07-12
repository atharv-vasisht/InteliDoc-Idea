from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import time

from app.core.database import get_async_db
from app.services.ai_service import ai_service
from app.schemas.ai import (
    ExtractionRequest, 
    ExtractionResponse, 
    SummarizationRequest, 
    SummarizationResponse
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