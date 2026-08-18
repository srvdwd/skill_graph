"""
The two "hard" queries for this project:

1. find_missing_skills  - a set-difference graph query (skill-gap analysis).
   In a relational schema this is a multi-table join plus a
   `NOT IN (subquery)` across a normalized Career-Skill junction table
   and a User-Skill junction table. Here it is one pattern match with
   a WHERE NOT EXISTS clause.

2. find_learning_path    - a variable-length path traversal
   (2+ hops, satisfies the multi-hop requirement). In SQL this needs a
   recursive CTE; here it's a single shortestPath() pattern.

Every query below is parameterized.
"""

from neo4j import Session


def get_career_title(session: Session, career_id: str) -> str | None:
    query = "MATCH (c:Career {id: $career_id}) RETURN c.title AS title"
    result = session.run(query, career_id=career_id).data()
    return result[0]["title"] if result else None


def get_required_skill_count(session: Session, career_id: str) -> int:
    query = """
        MATCH (c:Career {id: $career_id})-[:REQUIRES]->(s:Skill)
        RETURN count(s) AS total
    """
    result = session.run(query, career_id=career_id).data()
    return result[0]["total"] if result else 0


def find_missing_skills(session: Session, career_id: str, known_skill_ids: list[str]) -> list[dict]:
    """
    Skills REQUIRED by the target career that are NOT in the caller's
    known_skill_ids list. known_skill_ids is passed as a parameter list
    (never interpolated into the query string), and matched with
    `s.id IN $known_skill_ids`.
    """
    query = """
        MATCH (c:Career {id: $career_id})-[:REQUIRES]->(s:Skill)
        WHERE NOT s.id IN $known_skill_ids
        RETURN s.id AS id, s.name AS name, s.category AS category
        ORDER BY s.category, s.name
    """
    return session.run(query, career_id=career_id, known_skill_ids=known_skill_ids).data()


def get_resources_for_skills(session: Session, skill_ids: list[str]) -> dict[str, list[dict]]:
    """
    Learning resources that TEACH any of the given (missing) skills.
    Returns a dict keyed by skill_id so the service layer can attach
    each skill's resources without an extra query per skill.
    """
    query = """
        MATCH (r:Resource)-[:TEACHES]->(s:Skill)
        WHERE s.id IN $skill_ids
        RETURN s.id AS skill_id, r.id AS id, r.title AS title, r.url AS url, r.type AS type
        ORDER BY s.id, r.title
    """
    rows = session.run(query, skill_ids=skill_ids).data()

    resources_by_skill: dict[str, list[dict]] = {sid: [] for sid in skill_ids}
    for row in rows:
        resources_by_skill.setdefault(row["skill_id"], []).append(
            {"id": row["id"], "title": row["title"], "url": row["url"], "type": row["type"]}
        )
    return resources_by_skill


def find_learning_path(session: Session, from_skill_id: str, to_skill_id: str, max_hops: int = 6) -> dict:
    """
    Multi-hop traversal: the shortest chain of PREREQUISITE_FOR edges
    connecting from_skill_id to to_skill_id, e.g.
    Python -> Machine Learning -> Deep Learning -> LLM Applications.

    shortestPath() with a bounded variable-length pattern
    ([:PREREQUISITE_FOR*1..max_hops]) is the graph-native way to answer
    "how do I get from skill A to skill B" - the relational equivalent
    requires a recursive CTE with cycle detection.
    """
    query = """
        MATCH (from:Skill {id: $from_id}), (to:Skill {id: $to_id})
        MATCH path = shortestPath(
            (from)-[:PREREQUISITE_FOR*1..%d]->(to)
        )
        RETURN [node IN nodes(path) | {id: node.id, name: node.name}] AS path_nodes,
               length(path) AS hop_count
    """ % max_hops
    # NOTE: max_hops is a Python int controlled only by our own code
    # (never user input) and is inlined here because Neo4j does not
    # support parameterizing the bound of a variable-length relationship
    # pattern. from_id / to_id - the actual user-influenced values -
    # remain fully parameterized below.
    result = session.run(query, from_id=from_skill_id, to_id=to_skill_id).data()

    if not result:
        return {"path_found": False, "hop_count": 0, "path": []}

    record = result[0]
    return {
        "path_found": True,
        "hop_count": record["hop_count"],
        "path": record["path_nodes"],
    }


def find_indirect_skills_for_career(session: Session, career_id: str, max_hops: int = 3) -> list[dict]:
    """
    Skills reachable from a career's directly required skills via
    PREREQUISITE_FOR chains - i.e. skills that will eventually be
    needed even though the career doesn't require them directly.
    Another multi-hop traversal, useful for "what should I learn next
    after this".
    """
    query = """
        MATCH (c:Career {id: $career_id})-[:REQUIRES]->(:Skill)
              -[:PREREQUISITE_FOR*1..%d]->(indirect:Skill)
        WHERE NOT (c)-[:REQUIRES]->(indirect)
        RETURN DISTINCT indirect.id AS id, indirect.name AS name, indirect.category AS category
        ORDER BY indirect.name
    """ % max_hops
    return session.run(query, career_id=career_id).data()
