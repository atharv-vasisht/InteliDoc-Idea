from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import time
from app.core.database import get_async_db
from app.schemas.ai import SearchRequest, SearchResponse, SearchResult
from app.models.obligation import CategoryEnum, PriorityEnum

router = APIRouter()

@router.get("/", response_model=SearchResponse)
async def search_obligations(
    query: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, description="Maximum number of results"),
    category_filter: Optional[CategoryEnum] = Query(None, description="Filter by category"),
    priority_filter: Optional[PriorityEnum] = Query(None, description="Filter by priority"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Search obligations using semantic search
    """
    start_time = time.time()
    
    try:
        # TODO: Implement semantic search using Pinecone
        # For now, use basic text search
        
        # Build search query
        search_query = """
            SELECT o.*, d.title as document_title
            FROM obligations o
            JOIN documents d ON o.document_id = d.id
            WHERE LOWER(o.text) LIKE LOWER(:search_term)
        """
        
        params = {"search_term": f"%{query}%"}
        
        if category_filter:
            search_query += " AND o.category = :category"
            params["category"] = category_filter.value
            
        if priority_filter:
            search_query += " AND o.priority = :priority"
            params["priority"] = priority_filter.value
            
        search_query += " ORDER BY o.created_at DESC LIMIT :limit"
        params["limit"] = limit
        
        result = await db.execute(search_query, params)
        obligations = result.fetchall()
        
        # Convert to search results
        search_results = []
        for ob in obligations:
            # Calculate a simple similarity score (in production, use vector similarity)
            similarity_score = 0.8  # Placeholder
            
            search_results.append(SearchResult(
                obligation_id=ob.id,
                text=ob.text,
                category=CategoryEnum(ob.category),
                priority=PriorityEnum(ob.priority) if ob.priority else None,
                source_section=ob.source_section,
                document_title=ob.document_title,
                similarity_score=similarity_score
            ))
        
        processing_time = time.time() - start_time
        
        return SearchResponse(
            results=search_results,
            total_results=len(search_results),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching obligations: {str(e)}"
        ) 