from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_async_db
from app.schemas.mapping import Mapping, MappingCreate, MappingUpdate
from app.models.mapping import Mapping as MappingModel, MappingTypeEnum

router = APIRouter()

@router.post("/", response_model=Mapping)
async def create_mapping(
    mapping: MappingCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Create a new mapping
    """
    try:
        # TODO: Validate that obligation exists
        # TODO: Validate that user exists
        
        mapping_data = MappingModel(**mapping.dict())
        db.add(mapping_data)
        await db.commit()
        await db.refresh(mapping_data)
        
        return Mapping.from_orm(mapping_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating mapping: {str(e)}"
        )

@router.get("/", response_model=List[Mapping])
async def list_mappings(
    obligation_id: Optional[int] = Query(None, description="Filter by obligation ID"),
    mapping_type: Optional[MappingTypeEnum] = Query(None, description="Filter by mapping type"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    List mappings with optional filtering
    """
    try:
        # Build query
        query = "SELECT * FROM mappings WHERE 1=1"
        params = {}
        
        if obligation_id:
            query += " AND obligation_id = :obligation_id"
            params["obligation_id"] = obligation_id
            
        if mapping_type:
            query += " AND mapping_type = :mapping_type"
            params["mapping_type"] = mapping_type.value
            
        query += " ORDER BY created_at DESC"
        
        result = await db.execute(query, params)
        mappings = result.fetchall()
        
        return [
            Mapping(
                id=m.id,
                obligation_id=m.obligation_id,
                mapping_type=MappingTypeEnum(m.mapping_type),
                external_id=m.external_id,
                external_name=m.external_name,
                external_url=m.external_url,
                notes=m.notes,
                mapped_by=m.mapped_by,
                created_at=m.created_at.isoformat(),
                updated_at=m.updated_at.isoformat() if m.updated_at else None
            )
            for m in mappings
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching mappings: {str(e)}"
        )

@router.delete("/{mapping_id}")
async def delete_mapping(
    mapping_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Delete a mapping
    """
    try:
        result = await db.execute(
            "DELETE FROM mappings WHERE id = :id",
            {"id": mapping_id}
        )
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Mapping not found"
            )
        
        await db.commit()
        return {"message": "Mapping deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting mapping: {str(e)}"
        ) 