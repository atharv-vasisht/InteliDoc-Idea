from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os
import uuid
from datetime import datetime

from app.core.database import get_async_db
from app.core.config import settings
from app.schemas.document import DocumentCreate, Document, DocumentInDB
from app.models.document import Document as DocumentModel
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Upload a document (PDF, DOCX, TXT)
    """
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    try:
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # TODO: Upload to S3
        # For now, save locally (in production, use S3)
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Create document record
        # TODO: Extract text content using OCR/document processing
        document_data = DocumentCreate(
            title=title,
            filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            file_type=file_extension[1:],  # Remove the dot
            uploaded_by=1  # TODO: Get from auth
        )
        
        document = DocumentModel(**document_data.dict())
        db.add(document)
        await db.commit()
        await db.refresh(document)
        
        return Document.from_orm(document)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading document: {str(e)}"
        )

@router.get("/", response_model=List[Document])
async def list_documents(
    db: AsyncSession = Depends(get_async_db)
):
    """
    List all documents
    """
    try:
        # TODO: Add pagination and filtering
        result = await db.execute(
            "SELECT * FROM documents ORDER BY created_at DESC"
        )
        documents = result.fetchall()
        
        return [
            Document(
                id=doc.id,
                title=doc.title,
                filename=doc.filename,
                file_path=doc.file_path,
                file_size=doc.file_size,
                file_type=doc.file_type,
                content=doc.content,
                summary=doc.summary,
                uploaded_by=doc.uploaded_by,
                created_at=doc.created_at.isoformat(),
                updated_at=doc.updated_at.isoformat() if doc.updated_at else None
            )
            for doc in documents
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching documents: {str(e)}"
        )

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get a specific document by ID
    """
    try:
        result = await db.execute(
            "SELECT * FROM documents WHERE id = :id",
            {"id": document_id}
        )
        document = result.fetchone()
        
        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        return Document(
            id=document.id,
            title=document.title,
            filename=document.filename,
            file_path=document.file_path,
            file_size=document.file_size,
            file_type=document.file_type,
            content=document.content,
            summary=document.summary,
            uploaded_by=document.uploaded_by,
            created_at=document.created_at.isoformat(),
            updated_at=document.updated_at.isoformat() if document.updated_at else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching document: {str(e)}"
        ) 