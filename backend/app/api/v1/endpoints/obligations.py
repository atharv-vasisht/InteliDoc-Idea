from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_async_db
from app.schemas.obligation import Obligation, ObligationCreate, ObligationUpdate
from app.models.obligation import Obligation as ObligationModel, CategoryEnum, PriorityEnum

router = APIRouter()

@router.get("/", response_model=List[Obligation])
async def list_obligations(
    document_id: Optional[int] = Query(None, description="Filter by document ID"),
    category: Optional[CategoryEnum] = Query(None, description="Filter by category"),
    priority: Optional[PriorityEnum] = Query(None, description="Filter by priority"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    List obligations with optional filtering
    """
    try:
        # Build query
        query = "SELECT * FROM obligations WHERE 1=1"
        params = {}
        
        if document_id:
            query += " AND document_id = :document_id"
            params["document_id"] = document_id
            
        if category:
            query += " AND category = :category"
            params["category"] = category.value
            
        if priority:
            query += " AND priority = :priority"
            params["priority"] = priority.value
            
        query += " ORDER BY created_at DESC"
        
        result = await db.execute(query, params)
        obligations = result.fetchall()
        
        return [
            Obligation(
                id=ob.id,
                text=ob.text,
                category=CategoryEnum(ob.category),
                priority=PriorityEnum(ob.priority) if ob.priority else None,
                source_section=ob.source_section,
                confidence_score=ob.confidence_score,
                document_id=ob.document_id,
                extracted_by=ob.extracted_by,
                created_at=ob.created_at.isoformat(),
                updated_at=ob.updated_at.isoformat() if ob.updated_at else None
            )
            for ob in obligations
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching obligations: {str(e)}"
        )

@router.get("/{obligation_id}", response_model=Obligation)
async def get_obligation(
    obligation_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get a specific obligation by ID
    """
    try:
        result = await db.execute(
            "SELECT * FROM obligations WHERE id = :id",
            {"id": obligation_id}
        )
        obligation = result.fetchone()
        
        if not obligation:
            raise HTTPException(
                status_code=404,
                detail="Obligation not found"
            )
        
        return Obligation(
            id=obligation.id,
            text=obligation.text,
            category=CategoryEnum(obligation.category),
            priority=PriorityEnum(obligation.priority) if obligation.priority else None,
            source_section=obligation.source_section,
            confidence_score=obligation.confidence_score,
            document_id=obligation.document_id,
            extracted_by=obligation.extracted_by,
            created_at=obligation.created_at.isoformat(),
            updated_at=obligation.updated_at.isoformat() if obligation.updated_at else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching obligation: {str(e)}"
        )

@router.put("/{obligation_id}", response_model=Obligation)
async def update_obligation(
    obligation_id: int,
    updates: ObligationUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update an obligation
    """
    try:
        # Check if obligation exists
        result = await db.execute(
            "SELECT * FROM obligations WHERE id = :id",
            {"id": obligation_id}
        )
        obligation = result.fetchone()
        
        if not obligation:
            raise HTTPException(
                status_code=404,
                detail="Obligation not found"
            )
        
        # Build update query
        update_fields = []
        params = {"id": obligation_id}
        
        if updates.text is not None:
            update_fields.append("text = :text")
            params["text"] = updates.text
            
        if updates.category is not None:
            update_fields.append("category = :category")
            params["category"] = updates.category.value
            
        if updates.priority is not None:
            update_fields.append("priority = :priority")
            params["priority"] = updates.priority.value
            
        if updates.source_section is not None:
            update_fields.append("source_section = :source_section")
            params["source_section"] = updates.source_section
            
        if updates.confidence_score is not None:
            update_fields.append("confidence_score = :confidence_score")
            params["confidence_score"] = updates.confidence_score
        
        if not update_fields:
            raise HTTPException(
                status_code=400,
                detail="No fields to update"
            )
        
        update_fields.append("updated_at = NOW()")
        
        query = f"UPDATE obligations SET {', '.join(update_fields)} WHERE id = :id"
        await db.execute(query, params)
        await db.commit()
        
        # Return updated obligation
        return await get_obligation(obligation_id, db)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating obligation: {str(e)}"
        )

@router.delete("/{obligation_id}")
async def delete_obligation(
    obligation_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Delete an obligation
    """
    try:
        result = await db.execute(
            "DELETE FROM obligations WHERE id = :id",
            {"id": obligation_id}
        )
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Obligation not found"
            )
        
        await db.commit()
        return {"message": "Obligation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting obligation: {str(e)}"
        ) 