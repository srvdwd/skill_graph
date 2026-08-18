import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from neo4j.exceptions import ServiceUnavailable, Neo4jError

from app.db import get_session
from app.schemas.analysis import SkillGapRequest, SkillGapResponse, LearningPathResponse
from app.services import analysis_service

logger = logging.getLogger("skillgraph.analysis")
router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/skill-gap", response_model=SkillGapResponse)
def skill_gap(payload: SkillGapRequest, session=Depends(get_session)):
    """
    Given the skills a user already knows and a target career, returns
    the skills still missing, each annotated with learning resources.
    This is the core "awkward in SQL" set-difference graph query.
    """
    try:
        result = analysis_service.compute_skill_gap(
            session, payload.target_career_id, payload.known_skill_ids
        )
    except analysis_service.CareerNotFoundError:
        raise HTTPException(status_code=404, detail=f"Career '{payload.target_career_id}' not found")
    except (ServiceUnavailable, Neo4jError) as exc:
        logger.error("Skill gap analysis failed: %s", exc)
        raise HTTPException(status_code=503, detail="Database is currently unavailable")

    return result


@router.get("/learning-path", response_model=LearningPathResponse)
def learning_path(
    from_skill_id: str = Query(..., description="Skill the user already knows"),
    to_skill_id: str = Query(..., description="Skill the user wants to reach"),
    session=Depends(get_session),
):
    """
    Multi-hop traversal along PREREQUISITE_FOR edges, e.g.
    Python -> Machine Learning -> Deep Learning -> LLM Applications.
    """
    try:
        return analysis_service.compute_learning_path(session, from_skill_id, to_skill_id)
    except (ServiceUnavailable, Neo4jError) as exc:
        logger.error("Learning path query failed: %s", exc)
        raise HTTPException(status_code=503, detail="Database is currently unavailable")
