from neo4j import Session

from app.queries import analysis_queries


class CareerNotFoundError(Exception):
    pass


def compute_skill_gap(session: Session, target_career_id: str, known_skill_ids: list[str]) -> dict:
    career_title = analysis_queries.get_career_title(session, target_career_id)
    if career_title is None:
        raise CareerNotFoundError(f"Career '{target_career_id}' does not exist")

    required_count = analysis_queries.get_required_skill_count(session, target_career_id)
    missing_skills = analysis_queries.find_missing_skills(session, target_career_id, known_skill_ids)

    missing_ids = [s["id"] for s in missing_skills]
    resources_by_skill = analysis_queries.get_resources_for_skills(session, missing_ids)

    for skill in missing_skills:
        skill["resources"] = resources_by_skill.get(skill["id"], [])

    return {
        "target_career_id": target_career_id,
        "target_career_title": career_title,
        "required_skill_count": required_count,
        "known_skill_count": len(known_skill_ids),
        "missing_skills": missing_skills,
    }


def compute_learning_path(session: Session, from_skill_id: str, to_skill_id: str) -> dict:
    result = analysis_queries.find_learning_path(session, from_skill_id, to_skill_id)
    return {
        "from_skill_id": from_skill_id,
        "to_skill_id": to_skill_id,
        "path_found": result["path_found"],
        "hop_count": result["hop_count"],
        "path": result["path"],
    }
