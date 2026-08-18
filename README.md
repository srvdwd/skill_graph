# SkillGraph — Interactive Career & Skill Relationship Explorer

A full-stack app that models careers, skills, and their prerequisite relationships as a
graph in **CognoDB** (openCypher over Bolt, accessed via the official Neo4j Python driver),
lets a user select their existing skills, pick a target career, and see exactly which
skills are missing — plus learning resources and multi-hop learning paths between skills.

---

## 1. Stack

| Layer      | Technology                                                   |
|------------|---------------------------------------------------------------|
| Frontend   | React + Vite + Tailwind CSS                                   |
| Backend    | Python + FastAPI                                               |
| Database   | CognoDB (openCypher / Bolt)                                    |
| DB Driver  | Official `neo4j` Python driver                                 |
| Deployment | Vercel (frontend), Render/Railway (backend)                    |

---

## 2. Graph model

**Nodes:** `User`, `Skill`, `Career`, `Resource`

**Relationships:**
```
User    -[:HAS_SKILL]->        Skill
Career  -[:REQUIRES]->         Skill
Skill   -[:RELATED_TO]->       Skill
Skill   -[:PREREQUISITE_FOR]-> Skill
Resource-[:TEACHES]->          Skill
```

```
                       ┌────────────┐
                       │   Career   │
                       └─────┬──────┘
                             │ REQUIRES
                             ▼
   ┌──────────┐   PREREQUISITE_FOR   ┌──────────┐   PREREQUISITE_FOR   ┌────────────┐
   │  Skill A │ ───────────────────► │  Skill B │ ───────────────────► │  Skill C   │
   └────┬─────┘                      └────┬─────┘                     └─────┬──────┘
        │ RELATED_TO                      │ TEACHES (from Resource)         │
        ▼                                  ▲                                 ▲
   ┌──────────┐                      ┌──────────┐                     ┌────────────┐
   │  Skill D │                      │ Resource │                     │  Resource  │
   └──────────┘                      └──────────┘                     └────────────┘

           ┌──────────┐  HAS_SKILL
           │   User   │ ───────────► Skill
           └──────────┘
```

Real example chain seeded in the graph:
`Python → Machine Learning → Deep Learning → NLP → LLM Applications`

**Why each node/relationship exists:**
- `Career -[:REQUIRES]-> Skill`: the backbone of gap analysis — what a role needs.
- `Skill -[:PREREQUISITE_FOR]-> Skill`: directed ordering, powers multi-hop learning paths.
- `Skill -[:RELATED_TO]-> Skill`: lateral association (adjacent but not required-before).
- `Resource -[:TEACHES]-> Skill`: lets missing skills surface actionable learning material.
- `User -[:HAS_SKILL]-> Skill`: modeled but the current UI passes known-skill IDs directly
  in the gap-analysis request rather than persisting a logged-in user's selections —
  see "Known simplifications" below.

---

## 3. Repository layout

```
skillgraph/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, startup/shutdown, /api/health
│   │   ├── config.py        # env var loading (pydantic-settings)
│   │   ├── db.py            # Neo4j driver lifecycle + get_session() dependency
│   │   ├── routers/         # HTTP layer only (careers, skills, analysis)
│   │   ├── services/        # orchestration between routers and queries
│   │   ├── queries/         # every Cypher statement in the project lives here
│   │   └── schemas/         # Pydantic request/response models
│   ├── scripts/seed.py      # idempotent MERGE-based seed script
│   ├── requirements.txt
│   ├── render.yaml          # Render deployment blueprint
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── api/client.js    # single fetch wrapper for the backend
    │   ├── pages/           # CareerExplorer, SkillExplorer, GapAnalysis
    │   └── components/      # NavBar, SkillChip, LoadingState, EmptyState, ErrorState
    ├── vercel.json
    └── .env.example
```

---

## 4. Setup & run locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env with your real CognoDB URI / user / password

python scripts/seed.py          # loads careers, skills, resources, relationships

uvicorn app.main:app --reload   # http://localhost:8000
```

Open `http://localhost:8000/docs` for interactive Swagger UI, and check
`http://localhost:8000/api/health` to confirm the database connection.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env            # VITE_API_BASE_URL=http://localhost:8000
npm run dev                     # http://localhost:5173
```

---

## 5. API reference

| Method | Path                  | Purpose                                              |
|--------|-----------------------|-------------------------------------------------------|
| GET    | `/api/health`         | Reports API + database connectivity                   |
| GET    | `/api/careers`        | List all careers                                       |
| GET    | `/api/careers/{id}`   | One career + its required skills                       |
| GET    | `/api/skills`         | List all skills                                         |
| GET    | `/api/skills/{id}`    | One skill + its RELATED_TO / PREREQUISITE_FOR neighbors |
| POST   | `/api/skill-gap`      | Given known skills + target career → missing skills + resources |
| GET    | `/api/learning-path`  | Multi-hop shortest prerequisite path between two skills |

All bodies/params are validated with Pydantic; every Cypher query behind these
endpoints uses parameters (`$param`), never string concatenation.

---

## 6. Notable queries (interview talking points)

**Skill-gap analysis (`analysis_queries.find_missing_skills`)** — a set-difference:
skills a career `REQUIRES` minus the skills the user already has.
```cypher
MATCH (c:Career {id: $career_id})-[:REQUIRES]->(s:Skill)
WHERE NOT s.id IN $known_skill_ids
RETURN s.id AS id, s.name AS name, s.category AS category
```
In a relational schema this needs a `Career_Skill` junction table joined against a
`User_Skill` junction table with a `NOT IN` subquery. Here it's one pattern + one filter.

**Multi-hop learning path (`analysis_queries.find_learning_path`)** — variable-length
traversal along `PREREQUISITE_FOR` edges (2+ hops), e.g. Python → ML → Deep Learning → NLP:
```cypher
MATCH (from:Skill {id: $from_id}), (to:Skill {id: $to_id})
MATCH path = shortestPath((from)-[:PREREQUISITE_FOR*1..6]->(to))
RETURN [n IN nodes(path) | {id: n.id, name: n.name}] AS path_nodes, length(path) AS hop_count
```
The equivalent in SQL needs a recursive CTE with manual cycle detection. Note: the `*1..6`
hop bound is a hardcoded constant in our own code (Neo4j doesn't support parameterizing
variable-length pattern bounds) — `from_id`/`to_id`, the actual user-supplied values,
remain fully parameterized.

**Related careers by shared skills (`career_queries.get_related_careers`)** — another
graph-native query that's awkward relationally (self-join through a junction table +
`GROUP BY`/`HAVING`):
```cypher
MATCH (c1:Career {id: $career_id})-[:REQUIRES]->(s:Skill)<-[:REQUIRES]-(c2:Career)
WHERE c2.id <> c1.id
RETURN c2.id AS id, c2.title AS title, count(s) AS shared_skill_count
ORDER BY shared_skill_count DESC
```

---

## 7. Graceful failure handling

- The driver is created once at startup (`app/db.py`); `verify_connectivity()` is checked
  at boot and logged, but a failed check does **not** crash the process.
- Every router wraps its query calls in `try/except (ServiceUnavailable, Neo4jError)` and
  returns `503 { "detail": "Database is currently unavailable" }` instead of a raw 500.
- `/api/health` exposes live DB status so the frontend nav bar can show a
  connected/degraded indicator, polled every 15s.
- Verified manually: booting the API against an unreachable database still starts the
  server; `/api/health` returns `"degraded"`; `/api/careers` returns a clean `503`.

---

## 8. Deployment

**Frontend → Vercel:** import the `frontend/` folder as a Vite project (see `vercel.json`),
set `VITE_API_BASE_URL` to the deployed backend URL.

**Backend → Render/Railway:** deploy the `backend/` folder (see `render.yaml` for Render),
set `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `NEO4J_DATABASE`, and `ALLOWED_ORIGINS`
(the deployed frontend's URL) as environment variables. Run `python scripts/seed.py` once
against the production database before first use.

---

## 9. Known simplifications (worth naming proactively in an interview)

- No authentication layer — the `User` node and `HAS_SKILL` relationship are modeled in
  the schema, but the UI currently sends a user's selected skill IDs directly in the
  gap-analysis request rather than persisting them against a logged-in `User` node. This
  was a deliberate scope cut for a 48-hour assignment; wiring `HAS_SKILL` up would mean
  adding a login flow and a `POST /api/users/{id}/skills` endpoint using the same
  parameterized-Cypher pattern already used everywhere else.
- The `*1..6` hop bound in the learning-path query is a fixed constant, not user input —
  called out explicitly in code comments so it's clear this isn't a string-concatenation
  injection risk, just a Cypher language limitation (variable-length pattern bounds can't
  be parameterized).
- No caching layer — every request hits CognoDB directly. Fine at this data scale;
  worth mentioning as a next step for production traffic.
