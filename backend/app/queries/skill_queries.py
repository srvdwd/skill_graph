"""
All Cypher for the Skill domain. Every query is parameterized.
"""

from neo4j import Session


def get_all_skills(session: Session) -> list[dict]:
    query = """
        MATCH (s:Skill)
        RETURN s.id AS id, s.name AS name, s.category AS category, s.description AS description
        ORDER BY s.category, s.name
    """
    return session.run(query).data()


def get_skill_by_id(session: Session, skill_id: str) -> dict | None:
    query = """
        MATCH (s:Skill {id: $skill_id})
        RETURN s.id AS id, s.name AS name, s.category AS category, s.description AS description
    """
    result = session.run(query, skill_id=skill_id).data()
    return result[0] if result else None


def get_related_skills(session: Session, skill_id: str) -> list[dict]:
    """
    One-hop neighbors of a skill across both RELATED_TO (undirected,
    lateral relationship) and PREREQUISITE_FOR (directed, ordering
    relationship) edges. Tagging each row with the relationship type
    lets the frontend render them differently.
    """
    query = """
        MATCH (s:Skill {id: $skill_id})-[r:RELATED_TO|PREREQUISITE_FOR]-(other:Skill)
        RETURN other.id AS id, other.name AS name, type(r) AS relationship
        ORDER BY relationship, other.name
    """
    return session.run(query, skill_id=skill_id).data()
