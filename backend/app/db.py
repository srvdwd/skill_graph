
import logging
from typing import Generator

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError, Neo4jError

from app.config import get_settings

logger = logging.getLogger("skillgraph.db")

_driver: Driver | None = None


def init_driver() -> None:

    global _driver
    settings = get_settings()
    _driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    logger.info("Neo4j driver created for %s", settings.neo4j_uri)


def close_driver() -> None:

    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
        logger.info("Neo4j driver closed")


def verify_connectivity() -> tuple[bool, str | None]:

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

    if _driver is None:
        raise ServiceUnavailable("Database driver is not initialized")

    settings = get_settings()
    session = _driver.session(database=settings.neo4j_database)
    try:
        yield session
    finally:
        session.close()
