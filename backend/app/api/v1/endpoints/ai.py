from fastapi import APIRouter, HTTPException, Depends, Body
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