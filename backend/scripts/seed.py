
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from neo4j import GraphDatabase
from app.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skillgraph.seed")


CAREERS = [
    {"id": "career_data_analyst", "title": "Data Analyst",
     "description": "Analyzes structured data to find trends and support business decisions."},
    {"id": "career_backend_engineer", "title": "Backend Engineer",
     "description": "Builds and maintains server-side applications and APIs."},
    {"id": "career_data_scientist", "title": "Data Scientist",
     "description": "Builds statistical and machine learning models to solve business problems."},
    {"id": "career_ml_engineer", "title": "Machine Learning Engineer",
     "description": "Designs, trains, and deploys machine learning models in production."},
    {"id": "career_ai_engineer", "title": "AI Applications Engineer",
     "description": "Builds applications on top of large language models and AI APIs."},
    {"id": "career_devops_engineer", "title": "DevOps Engineer",
     "description": "Automates deployment pipelines and manages cloud infrastructure."},
    {"id": "career_frontend_engineer", "title": "Frontend Engineer",
     "description": "Builds user-facing web interfaces and client-side applications."},
]

SKILLS = [
    # Foundations
    {"id": "skill_python", "name": "Python", "category": "Programming",
     "description": "General-purpose programming language widely used in data and backend work."},
    {"id": "skill_sql", "name": "SQL", "category": "Data",
     "description": "Query language for relational databases."},
    {"id": "skill_statistics", "name": "Statistics", "category": "Math",
     "description": "Foundations of probability, distributions, and inference."},
    {"id": "skill_linear_algebra", "name": "Linear Algebra", "category": "Math",
     "description": "Vectors, matrices, and transformations underpinning ML algorithms."},
    {"id": "skill_git", "name": "Git", "category": "Tools",
     "description": "Version control system for tracking code changes."},

    # Data analysis
    {"id": "skill_excel", "name": "Excel", "category": "Data",
     "description": "Spreadsheet tool for data manipulation and reporting."},
    {"id": "skill_data_visualization", "name": "Data Visualization", "category": "Data",
     "description": "Communicating data insights through charts and dashboards."},
    {"id": "skill_dashboarding", "name": "Dashboarding (BI Tools)", "category": "Data",
     "description": "Building interactive dashboards with tools like Tableau or Power BI."},

    # ML / AI path
    {"id": "skill_pandas", "name": "Pandas", "category": "Data",
     "description": "Python library for tabular data manipulation."},
    {"id": "skill_machine_learning", "name": "Machine Learning", "category": "AI/ML",
     "description": "Building models that learn patterns from data."},
    {"id": "skill_deep_learning", "name": "Deep Learning", "category": "AI/ML",
     "description": "Neural network based machine learning."},
    {"id": "skill_nlp", "name": "Natural Language Processing", "category": "AI/ML",
     "description": "Techniques for processing and understanding human language."},
    {"id": "skill_llm_applications", "name": "LLM Applications", "category": "AI/ML",
     "description": "Building applications on top of large language models."},
    {"id": "skill_model_deployment", "name": "Model Deployment", "category": "AI/ML",
     "description": "Serving trained ML models in production environments."},
    {"id": "skill_mlops", "name": "MLOps", "category": "AI/ML",
     "description": "Practices for operating and monitoring ML systems in production."},
    {"id": "skill_prompt_engineering", "name": "Prompt Engineering", "category": "AI/ML",
     "description": "Designing effective prompts to guide LLM behavior."},
    {"id": "skill_vector_databases", "name": "Vector Databases", "category": "AI/ML",
     "description": "Databases optimized for similarity search over embeddings."},

    # Backend
    {"id": "skill_rest_apis", "name": "REST APIs", "category": "Backend",
     "description": "Designing and building HTTP-based web APIs."},
    {"id": "skill_databases", "name": "Database Design", "category": "Backend",
     "description": "Designing normalized relational schemas."},
    {"id": "skill_graph_databases", "name": "Graph Databases", "category": "Backend",
     "description": "Modeling and querying connected data with graph databases."},
    {"id": "skill_authentication", "name": "Authentication & Authorization", "category": "Backend",
     "description": "Implementing secure login and access control."},
    {"id": "skill_system_design", "name": "System Design", "category": "Backend",
     "description": "Designing scalable, maintainable software architectures."},

    # DevOps
    {"id": "skill_docker", "name": "Docker", "category": "DevOps",
     "description": "Containerizing applications for consistent deployment."},
    {"id": "skill_ci_cd", "name": "CI/CD", "category": "DevOps",
     "description": "Automating build, test, and deployment pipelines."},
    {"id": "skill_cloud_platforms", "name": "Cloud Platforms (AWS/GCP/Azure)", "category": "DevOps",
     "description": "Provisioning and managing infrastructure in the cloud."},
    {"id": "skill_kubernetes", "name": "Kubernetes", "category": "DevOps",
     "description": "Orchestrating containerized workloads at scale."},
    {"id": "skill_monitoring", "name": "Monitoring & Observability", "category": "DevOps",
     "description": "Tracking system health, logs, and metrics in production."},

    # Frontend
    {"id": "skill_html_css", "name": "HTML/CSS", "category": "Frontend",
     "description": "Structuring and styling web pages."},
    {"id": "skill_javascript", "name": "JavaScript", "category": "Frontend",
     "description": "Scripting language for interactive web pages."},
    {"id": "skill_react", "name": "React", "category": "Frontend",
     "description": "Component-based library for building user interfaces."},
    {"id": "skill_state_management", "name": "State Management", "category": "Frontend",
     "description": "Managing application state in complex UIs."},
    {"id": "skill_responsive_design", "name": "Responsive Design", "category": "Frontend",
     "description": "Building UIs that adapt to different screen sizes."},
]

RESOURCES = [
    {"id": "res_python_crash_course", "title": "Python Crash Course", "url": "https://example.com/python-crash-course", "type": "Book"},
    {"id": "res_sql_for_data", "title": "SQL for Data Analysis", "url": "https://example.com/sql-for-data", "type": "Course"},
    {"id": "res_stats_khan", "title": "Statistics Fundamentals", "url": "https://example.com/statistics-fundamentals", "type": "Course"},
    {"id": "res_linear_algebra_essence", "title": "Essence of Linear Algebra", "url": "https://example.com/essence-of-linear-algebra", "type": "Video Series"},
    {"id": "res_git_handbook", "title": "Git Handbook", "url": "https://example.com/git-handbook", "type": "Article"},
    {"id": "res_excel_dashboards", "title": "Excel for Business Analysis", "url": "https://example.com/excel-business-analysis", "type": "Course"},
    {"id": "res_dataviz_storytelling", "title": "Storytelling with Data", "url": "https://example.com/storytelling-with-data", "type": "Book"},
    {"id": "res_powerbi_guide", "title": "Power BI Complete Guide", "url": "https://example.com/power-bi-guide", "type": "Course"},
    {"id": "res_pandas_docs", "title": "Pandas in 10 Minutes", "url": "https://example.com/pandas-10-minutes", "type": "Tutorial"},
    {"id": "res_ml_course_andrew_ng", "title": "Machine Learning Specialization", "url": "https://example.com/ml-specialization", "type": "Course"},
    {"id": "res_deep_learning_book", "title": "Deep Learning", "url": "https://example.com/deep-learning-book", "type": "Book"},
    {"id": "res_nlp_with_transformers", "title": "NLP with Transformers", "url": "https://example.com/nlp-with-transformers", "type": "Book"},
    {"id": "res_llm_app_building", "title": "Building LLM Applications", "url": "https://example.com/building-llm-apps", "type": "Course"},
    {"id": "res_prompt_engineering_guide", "title": "Prompt Engineering Guide", "url": "https://example.com/prompt-engineering-guide", "type": "Article"},
    {"id": "res_vector_db_intro", "title": "Introduction to Vector Databases", "url": "https://example.com/vector-db-intro", "type": "Article"},
    {"id": "res_mlops_specialization", "title": "MLOps Specialization", "url": "https://example.com/mlops-specialization", "type": "Course"},
    {"id": "res_model_serving_guide", "title": "Serving ML Models in Production", "url": "https://example.com/model-serving", "type": "Article"},
    {"id": "res_rest_api_design", "title": "REST API Design Rulebook", "url": "https://example.com/rest-api-design", "type": "Book"},
    {"id": "res_db_design_fundamentals", "title": "Database Design Fundamentals", "url": "https://example.com/db-design-fundamentals", "type": "Course"},
    {"id": "res_graph_db_guide", "title": "Graph Databases in Action", "url": "https://example.com/graph-databases-in-action", "type": "Book"},
    {"id": "res_docker_deep_dive", "title": "Docker Deep Dive", "url": "https://example.com/docker-deep-dive", "type": "Book"},
    {"id": "res_kubernetes_up_running", "title": "Kubernetes Up & Running", "url": "https://example.com/kubernetes-up-running", "type": "Book"},
    {"id": "res_react_official_docs", "title": "React Official Documentation", "url": "https://react.dev/learn", "type": "Docs"},
    {"id": "res_javascript_the_hard_parts", "title": "JavaScript: The Hard Parts", "url": "https://example.com/js-hard-parts", "type": "Course"},
]

# Career -[:REQUIRES]-> Skill
CAREER_REQUIRES_SKILL = [
    ("career_data_analyst", ["skill_excel", "skill_sql", "skill_statistics", "skill_data_visualization", "skill_dashboarding"]),
    ("career_backend_engineer", ["skill_python", "skill_sql", "skill_git", "skill_rest_apis", "skill_databases", "skill_authentication", "skill_system_design"]),
    ("career_data_scientist", ["skill_python", "skill_sql", "skill_statistics", "skill_linear_algebra", "skill_pandas", "skill_machine_learning", "skill_data_visualization"]),
    ("career_ml_engineer", ["skill_python", "skill_statistics", "skill_linear_algebra", "skill_machine_learning", "skill_deep_learning", "skill_model_deployment", "skill_mlops", "skill_docker"]),
    ("career_ai_engineer", ["skill_python", "skill_rest_apis", "skill_llm_applications", "skill_prompt_engineering", "skill_vector_databases", "skill_nlp"]),
    ("career_devops_engineer", ["skill_git", "skill_docker", "skill_ci_cd", "skill_cloud_platforms", "skill_kubernetes", "skill_monitoring"]),
    ("career_frontend_engineer", ["skill_html_css", "skill_javascript", "skill_react", "skill_state_management", "skill_responsive_design", "skill_git"]),
]

# Skill -[:PREREQUISITE_FOR]-> Skill  (directed, ordering relationship)
SKILL_PREREQUISITE_FOR = [
    ("skill_python", "skill_pandas"),
    ("skill_python", "skill_machine_learning"),
    ("skill_python", "skill_rest_apis"),
    ("skill_statistics", "skill_machine_learning"),
    ("skill_linear_algebra", "skill_machine_learning"),
    ("skill_pandas", "skill_machine_learning"),
    ("skill_machine_learning", "skill_deep_learning"),
    ("skill_deep_learning", "skill_nlp"),
    ("skill_nlp", "skill_llm_applications"),
    ("skill_llm_applications", "skill_prompt_engineering"),
    ("skill_prompt_engineering", "skill_vector_databases"),
    ("skill_machine_learning", "skill_model_deployment"),
    ("skill_model_deployment", "skill_mlops"),
    ("skill_docker", "skill_mlops"),
    ("skill_docker", "skill_kubernetes"),
    ("skill_git", "skill_ci_cd"),
    ("skill_ci_cd", "skill_kubernetes"),
    ("skill_sql", "skill_databases"),
    ("skill_databases", "skill_system_design"),
    ("skill_rest_apis", "skill_authentication"),
    ("skill_authentication", "skill_system_design"),
    ("skill_html_css", "skill_javascript"),
    ("skill_javascript", "skill_react"),
    ("skill_react", "skill_state_management"),
    ("skill_html_css", "skill_responsive_design"),
    ("skill_excel", "skill_data_visualization"),
    ("skill_sql", "skill_data_visualization"),
    ("skill_data_visualization", "skill_dashboarding"),
]

# Skill -[:RELATED_TO]-> Skill  (undirected-in-spirit lateral association)
SKILL_RELATED_TO = [
    ("skill_python", "skill_sql"),
    ("skill_machine_learning", "skill_statistics"),
    ("skill_deep_learning", "skill_linear_algebra"),
    ("skill_docker", "skill_cloud_platforms"),
    ("skill_kubernetes", "skill_cloud_platforms"),
    ("skill_monitoring", "skill_cloud_platforms"),
    ("skill_react", "skill_javascript"),
    ("skill_state_management", "skill_javascript"),
    ("skill_rest_apis", "skill_databases"),
    ("skill_graph_databases", "skill_databases"),
    ("skill_vector_databases", "skill_graph_databases"),
    ("skill_data_visualization", "skill_pandas"),
    ("skill_mlops", "skill_ci_cd"),
]

# Resource -[:TEACHES]-> Skill
RESOURCE_TEACHES_SKILL = [
    ("res_python_crash_course", "skill_python"),
    ("res_sql_for_data", "skill_sql"),
    ("res_stats_khan", "skill_statistics"),
    ("res_linear_algebra_essence", "skill_linear_algebra"),
    ("res_git_handbook", "skill_git"),
    ("res_excel_dashboards", "skill_excel"),
    ("res_dataviz_storytelling", "skill_data_visualization"),
    ("res_powerbi_guide", "skill_dashboarding"),
    ("res_pandas_docs", "skill_pandas"),
    ("res_ml_course_andrew_ng", "skill_machine_learning"),
    ("res_deep_learning_book", "skill_deep_learning"),
    ("res_nlp_with_transformers", "skill_nlp"),
    ("res_llm_app_building", "skill_llm_applications"),
    ("res_prompt_engineering_guide", "skill_prompt_engineering"),
    ("res_vector_db_intro", "skill_vector_databases"),
    ("res_mlops_specialization", "skill_mlops"),
    ("res_model_serving_guide", "skill_model_deployment"),
    ("res_rest_api_design", "skill_rest_apis"),
    ("res_db_design_fundamentals", "skill_databases"),
    ("res_graph_db_guide", "skill_graph_databases"),
    ("res_docker_deep_dive", "skill_docker"),
    ("res_kubernetes_up_running", "skill_kubernetes"),
    ("res_react_official_docs", "skill_react"),
    ("res_javascript_the_hard_parts", "skill_javascript"),
]


# ---------------------------------------------------------------------------
# Constraints (idempotent - CREATE CONSTRAINT IF NOT EXISTS)
# ---------------------------------------------------------------------------

CONSTRAINTS = [
    "CREATE CONSTRAINT career_id_unique IF NOT EXISTS FOR (c:Career) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT skill_id_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT resource_id_unique IF NOT EXISTS FOR (r:Resource) REQUIRE r.id IS UNIQUE",
    "CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
]


def apply_constraints(session):
    for statement in CONSTRAINTS:
        session.run(statement)
    logger.info("Constraints applied (%d)", len(CONSTRAINTS))


def seed_nodes(session, label: str, rows: list[dict]):
    """
    Generic idempotent node loader. UNWIND turns the parameter list into
    rows inside a single Cypher statement (one round trip, not one query
    per node), and MERGE on id prevents duplicates on re-run.
    """
    query = f"""
        UNWIND $rows AS row
        MERGE (n:{label} {{id: row.id}})
        SET n += row
    """
    session.run(query, rows=rows)
    logger.info("Merged %d %s nodes", len(rows), label)


def seed_career_requires_skill(session, pairs):
    rows = [{"career_id": c, "skill_id": s} for c, skills in pairs for s in skills]
    query = """
        UNWIND $rows AS row
        MATCH (c:Career {id: row.career_id})
        MATCH (s:Skill {id: row.skill_id})
        MERGE (c)-[:REQUIRES]->(s)
    """
    session.run(query, rows=rows)
    logger.info("Merged %d REQUIRES relationships", len(rows))


def seed_skill_relationship(session, pairs, rel_type: str):
    rows = [{"from_id": a, "to_id": b} for a, b in pairs]
    query = f"""
        UNWIND $rows AS row
        MATCH (a:Skill {{id: row.from_id}})
        MATCH (b:Skill {{id: row.to_id}})
        MERGE (a)-[:{rel_type}]->(b)
    """
    session.run(query, rows=rows)
    logger.info("Merged %d %s relationships", len(rows), rel_type)


def seed_resource_teaches_skill(session, pairs):
    rows = [{"resource_id": r, "skill_id": s} for r, s in pairs]
    query = """
        UNWIND $rows AS row
        MATCH (r:Resource {id: row.resource_id})
        MATCH (s:Skill {id: row.skill_id})
        MERGE (r)-[:TEACHES]->(s)
    """
    session.run(query, rows=rows)
    logger.info("Merged %d TEACHES relationships", len(rows))


def main():
    settings = get_settings()
    driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))

    try:
        driver.verify_connectivity()
        logger.info("Connected to CognoDB at %s", settings.neo4j_uri)

        with driver.session(database=settings.neo4j_database) as session:
            apply_constraints(session)
            seed_nodes(session, "Career", CAREERS)
            seed_nodes(session, "Skill", SKILLS)
            seed_nodes(session, "Resource", RESOURCES)

            seed_career_requires_skill(session, CAREER_REQUIRES_SKILL)
            seed_skill_relationship(session, SKILL_PREREQUISITE_FOR, "PREREQUISITE_FOR")
            seed_skill_relationship(session, SKILL_RELATED_TO, "RELATED_TO")
            seed_resource_teaches_skill(session, RESOURCE_TEACHES_SKILL)

        logger.info("Seed complete.")
    except Exception as exc:
        logger.error("Seed failed: %s", exc)
        raise
    finally:
        driver.close()


if __name__ == "__main__":
    main()
