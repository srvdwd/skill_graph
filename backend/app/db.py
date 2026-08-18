"""
Owns the lifecycle of the single Neo4j driver instance used to talk to
CognoDB over Bolt. Created once at app startup, reused for every
request, closed once at shutdown.

No other module should import `neo4j` directly for connection purposes -
everything goes through get_session() below. That is what makes
"handle database connection failures gracefully" a one-place concern.
"""

import logging
from typing import Generator

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError, Neo4jError

from app.config import get_settings

logger = logging.getLogger("skillgraph.db")

_driver: Driver | None = None


def init_driver() -> None:
    """Create the driver once, at FastAPI startup."""
    global _driver
    settings = get_settings()
    _driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    logger.info("Neo4j driver created for %s", settings.neo4j_uri)


def close_driver() -> None:
    """Close the driver once, at FastAPI shutdown."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
        logger.info("Neo4j driver closed")


def verify_connectivity() -> tuple[bool, str | None]:
    """
    Actively checks that CognoDB is reachable and credentials are valid.
    Returns (is_healthy, error_message).
    Used by /api/health and at startup so failures surface immediately
    instead of on the first user request.
    """
    if _driver is None:
        return False, "Driver not initialized"
    try:
        _driver.verify_connectivity()
        return True, None
    except AuthError as exc:
        logger.error("CognoDB auth failed: %s", exc)
        return False, "Authentication with the database failed"
    except ServiceUnavailable as exc:
        logger.error("CognoDB unreachable: %s", exc)
        return False, "Database is unreachable"
    except Neo4jError as exc:
        logger.error("CognoDB error: %s", exc)
        return False, "Unexpected database error"


def get_session() -> Generator:
    """
    FastAPI dependency. Yields a Neo4j session scoped to the configured
    database, and always closes it - even if the request raised.
    Routers/services never construct sessions themselves.
    """
    if _driver is None:
        raise ServiceUnavailable("Database driver is not initialized")

    settings = get_settings()
    session = _driver.session(database=settings.neo4j_database)
    try:
        yield session
    finally:
        session.close()
