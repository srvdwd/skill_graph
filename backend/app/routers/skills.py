import logging

from fastapi import APIRouter, Depends, HTTPException
from neo4j.exceptions import ServiceUnavailable, Neo4jError

from app.db import get_session
from app.schemas.skill import SkillSummary, SkillDetail
from app.services import skill_service

logger = logging.getLogger("skillgraph.skills")
router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("", response_model=list[SkillSummary])
def list_skills(session=Depends(get_session)):
    """Returns every skill in the graph."""
    try:
        return skill_service.list_skills(session)
    except (ServiceUnavailable, Neo4jError) as exc:
        logger.error("Failed to list skills: %s", exc)
        raise HTTPException(status_code=503, detail="Database is currently unavailable")


@router.get("/{skill_id}", response_model=SkillDetail)
def get_skill(skill_id: str, session=Depends(get_session)):
    """Returns one skill plus its RELATED_TO / PREREQUISITE_FOR neighbors."""
    try:
        skill = skill_service.get_skill_detail(session, skill_id)
    except (ServiceUnavailable, Neo4jError) as exc:
        logger.error("Failed to fetch skill %s: %s", skill_id, exc)
        raise HTTPException(status_code=503, detail="Database is currently unavailable")

    if skill is None:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    return skill
