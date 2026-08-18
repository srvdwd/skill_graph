import logging

from fastapi import APIRouter, Depends, HTTPException
from neo4j.exceptions import ServiceUnavailable, Neo4jError

from app.db import get_session
from app.schemas.career import CareerSummary, CareerDetail
from app.services import career_service

logger = logging.getLogger("skillgraph.careers")
router = APIRouter(prefix="/api/careers", tags=["careers"])


@router.get("", response_model=list[CareerSummary])
def list_careers(session=Depends(get_session)):
    """Returns every career role in the graph."""
    try:
        return career_service.list_careers(session)
    except (ServiceUnavailable, Neo4jError) as exc:
        logger.error("Failed to list careers: %s", exc)
        raise HTTPException(status_code=503, detail="Database is currently unavailable")


@router.get("/{career_id}", response_model=CareerDetail)
def get_career(career_id: str, session=Depends(get_session)):
    """Returns one career plus the full list of skills it REQUIRES."""
    try:
        career = career_service.get_career_detail(session, career_id)
    except (ServiceUnavailable, Neo4jError) as exc:
        logger.error("Failed to fetch career %s: %s", career_id, exc)
        raise HTTPException(status_code=503, detail="Database is currently unavailable")

    if career is None:
        raise HTTPException(status_code=404, detail=f"Career '{career_id}' not found")
    return career
