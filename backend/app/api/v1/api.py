from fastapi import APIRouter
from app.api.v1.endpoints import documents, obligations, mappings, ai, search, reports

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(obligations.router, prefix="/obligations", tags=["obligations"])
api_router.include_router(mappings.router, prefix="/mappings", tags=["mappings"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"]) 