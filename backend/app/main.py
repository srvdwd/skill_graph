import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app import db
from app.routers import careers, skills, analysis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skillgraph.main")

app = FastAPI(
    title="SkillGraph API",
    description="Career and skill relationship explorer backed by CognoDB (openCypher/Bolt)",
    version="1.0.0",
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(careers.router)
app.include_router(skills.router)
app.include_router(analysis.router)


@app.on_event("startup")
def on_startup():
    db.init_driver()
    healthy, error = db.verify_connectivity()
    if healthy:
        logger.info("Connected to CognoDB successfully")
    else:
        # Do not crash the process - the API should still start and report
        # its unhealthy state via /api/health rather than fail to boot.
        logger.warning("Could not verify CognoDB connectivity at startup: %s", error)


@app.on_event("shutdown")
def on_shutdown():
    db.close_driver()


@app.get("/api/health", tags=["health"])
def health_check():
    """
    Reports whether the API process is up AND whether it can currently
    reach CognoDB. Frontend can poll this to distinguish "backend down"
    from "backend up, database down".
    """
    healthy, error = db.verify_connectivity()
    return {
        "status": "ok" if healthy else "degraded",
        "database_connected": healthy,
        "database_error": error,
    }
