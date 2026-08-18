from neo4j import Session

from app.queries import career_queries


def list_careers(session: Session) -> list[dict]:
    return career_queries.get_all_careers(session)


def get_career_detail(session: Session, career_id: str) -> dict | None:
    return career_queries.get_career_by_id(session, career_id)
