from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from app.core.database import get_async_db

router = APIRouter()

@router.get("/gap-analysis")
async def generate_gap_analysis(
    document_id: Optional[int] = Query(None, description="Filter by document ID"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Generate gap analysis report showing unmapped obligations
    """
    try:
        # Build query to get obligations and their mapping status
        query = """
            SELECT 
                o.id,
                o.text,
                o.category,
                o.priority,
                o.source_section,
                d.title as document_title,
                COUNT(m.id) as mapping_count
            FROM obligations o
            JOIN documents d ON o.document_id = d.id
            LEFT JOIN mappings m ON o.id = m.obligation_id
        """
        
        params = {}
        if document_id:
            query += " WHERE o.document_id = :document_id"
            params["document_id"] = document_id
            
        query += """
            GROUP BY o.id, o.text, o.category, o.priority, o.source_section, d.title
            ORDER BY mapping_count ASC, o.created_at DESC
        """
        
        result = await db.execute(query, params)
        obligations = result.fetchall()
        
        # Categorize obligations
        mapped_obligations = []
        unmapped_obligations = []
        
        for ob in obligations:
            obligation_data = {
                "id": ob.id,
                "text": ob.text,
                "category": ob.category,
                "priority": ob.priority,
                "source_section": ob.source_section,
                "document_title": ob.document_title,
                "mapping_count": ob.mapping_count
            }
            
            if ob.mapping_count > 0:
                mapped_obligations.append(obligation_data)
            else:
                unmapped_obligations.append(obligation_data)
        
        # Calculate statistics
        total_obligations = len(obligations)
        total_mapped = len(mapped_obligations)
        total_unmapped = len(unmapped_obligations)
        mapping_rate = (total_mapped / total_obligations * 100) if total_obligations > 0 else 0
        
        # Category breakdown
        category_stats = {}
        for ob in obligations:
            category = ob.category
            if category not in category_stats:
                category_stats[category] = {"total": 0, "mapped": 0, "unmapped": 0}
            
            category_stats[category]["total"] += 1
            if ob.mapping_count > 0:
                category_stats[category]["mapped"] += 1
            else:
                category_stats[category]["unmapped"] += 1
        
        # Priority breakdown
        priority_stats = {}
        for ob in obligations:
            priority = ob.priority or "unknown"
            if priority not in priority_stats:
                priority_stats[priority] = {"total": 0, "mapped": 0, "unmapped": 0}
            
            priority_stats[priority]["total"] += 1
            if ob.mapping_count > 0:
                priority_stats[priority]["mapped"] += 1
            else:
                priority_stats[priority]["unmapped"] += 1
        
        return {
            "summary": {
                "total_obligations": total_obligations,
                "total_mapped": total_mapped,
                "total_unmapped": total_unmapped,
                "mapping_rate_percentage": round(mapping_rate, 2)
            },
            "category_breakdown": category_stats,
            "priority_breakdown": priority_stats,
            "unmapped_obligations": unmapped_obligations,
            "mapped_obligations": mapped_obligations,
            "generated_at": "2024-01-01T00:00:00Z"  # TODO: Use actual timestamp
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating gap analysis: {str(e)}"
        )

@router.get("/mapping-summary")
async def get_mapping_summary(
    document_id: Optional[int] = Query(None, description="Filter by document ID"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get summary of mappings by type
    """
    try:
        query = """
            SELECT 
                m.mapping_type,
                COUNT(*) as count,
                COUNT(DISTINCT m.obligation_id) as unique_obligations
            FROM mappings m
        """
        
        params = {}
        if document_id:
            query += """
                JOIN obligations o ON m.obligation_id = o.id
                WHERE o.document_id = :document_id
            """
            params["document_id"] = document_id
            
        query += " GROUP BY m.mapping_type ORDER BY count DESC"
        
        result = await db.execute(query, params)
        mappings = result.fetchall()
        
        return {
            "mapping_summary": [
                {
                    "mapping_type": m.mapping_type,
                    "total_mappings": m.count,
                    "unique_obligations": m.unique_obligations
                }
                for m in mappings
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating mapping summary: {str(e)}"
        ) 