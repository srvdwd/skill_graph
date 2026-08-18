"""
All Cypher for the Career domain. Every query is parameterized -
no f-strings or string concatenation are used to build Cypher.
"""

from neo4j import Session


def get_all_careers(session: Session) -> list[dict]:
    query = """
        MATCH (c:Career)
        RETURN c.id AS id, c.title AS title, c.description AS description
        ORDER BY c.title
    """
    return session.run(query).data()


def get_career_by_id(session: Session, career_id: str) -> dict | None:
    """
    Returns the career plus every skill it REQUIRES, in one round trip.
    collect() turns the fanned-out (career)-[:REQUIRES]->(skill) rows
    back into a single row with a list of skills.
    """
    query = """
        MATCH (c:Career {id: $career_id})
        OPTIONAL MATCH (c)-[:REQUIRES]->(s:Skill)
        RETURN c.id AS id,
               c.title AS title,
               c.description AS description,
               collect({id: s.id, name: s.name, category: s.category}) AS required_skills
    """
    result = session.run(query, career_id=career_id).data()
    if not result:
        return None

    record = result[0]
    # OPTIONAL MATCH with no matches yields a single null-filled skill row - filter it out
    record["required_skills"] = [s for s in record["required_skills"] if s.get("id")]
    return record


def get_related_careers(session: Session, career_id: str, limit: int = 5) -> list[dict]:
    """
    Careers that share required skills with the given career, ranked by
    how many skills they share. This is the "awkward in SQL" query:
    in a relational model this is a self-join through a junction table
    with a GROUP BY + HAVING; here it's one pattern match.
    """
    query = """
        MATCH (c1:Career {id: $career_id})-[:REQUIRES]->(s:Skill)<-[:REQUIRES]-(c2:Career)
        WHERE c2.id <> c1.id
        RETURN c2.id AS id, c2.title AS title, count(s) AS shared_skill_count
        ORDER BY shared_skill_count DESC
        LIMIT $limit
    """
    return session.run(query, career_id=career_id, limit=limit).data()
