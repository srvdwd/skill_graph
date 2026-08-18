from neo4j import Session

from app.queries import skill_queries


def list_skills(session: Session) -> list[dict]:
    return skill_queries.get_all_skills(session)


def get_skill_detail(session: Session, skill_id: str) -> dict | None:
    skill = skill_queries.get_skill_by_id(session, skill_id)
    if skill is None:
        return None

    skill["related_skills"] = skill_queries.get_related_skills(session, skill_id)
    return skill
