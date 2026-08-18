# 🚀 SkillGraph — Interactive Career & Skill Relationship Explorer

<p align="center">
  <strong>Turn skills into career paths.</strong><br/>
  Explore careers, discover skill gaps, and navigate prerequisite relationships through a graph-powered experience.
</p>

<p align="center">
  <a href="https://skillgraph-self.vercel.app/">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Vercel-000000?style=for-the-badge" alt="Live Demo"/>
  </a>
  <a href="https://skillgraph-0izb.onrender.com/docs">
    <img src="https://img.shields.io/badge/⚡_API-Swagger-009688?style=for-the-badge" alt="API Docs"/>
  </a>
  <img src="https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="Frontend"/>
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="Backend"/>
  <img src="https://img.shields.io/badge/Database-CognoDB-FF6B35?style=for-the-badge" alt="Database"/>
</p>

---

## 🔗 Live Application

| Service | URL |
|---|---|
| 🌐 **Frontend** | https://skillgraph-self.vercel.app/ |
| ⚡ **Backend API** | https://skillgraph-0izb.onrender.com |
| 📚 **Swagger / OpenAPI** | https://skillgraph-0izb.onrender.com/docs |
| ❤️ **Health Check** | https://skillgraph-0izb.onrender.com/api/health |

> **Tip:** Open the Swagger URL to explore and execute the API endpoints interactively.

---

## 🎥 Project Demo Video

Watch the complete SkillGraph walkthrough, including the deployed application and its main functionality:

▶️ **[Watch the SkillGraph Demo on Google Drive](https://drive.google.com/file/d/1JLse8BtWF5V_rDBSI-rtD7YXAdFbR12a/view?usp=sharing)**

The demo covers the core user experience, including career exploration, skill exploration, skill-gap analysis, and learning-path functionality.

---

## ✨ What is SkillGraph?

SkillGraph is a full-stack career exploration application that represents **careers, skills, resources, and their relationships as a graph** in **CognoDB**.

Instead of treating career requirements as isolated lists, SkillGraph models the connections between skills so that useful graph traversals can answer questions such as:

- What skills does a career require?
- Which skills am I missing for a target role?
- Which skills are prerequisites for another skill?
- What is the shortest prerequisite learning path between two skills?
- Which other careers share skills with my target career?
- Which learning resources can help with a missing skill?

The graph is accessed through **openCypher over Bolt** using the official **Neo4j Python driver**.

---

## 🧭 Core User Flow

```text
                    ┌───────────────────┐
                    │   Choose Career   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Explore Required  │
                    │      Skills       │
                    └─────────┬─────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
      ┌───────────────────┐       ┌───────────────────┐
      │ Select Your Skills│       │ Explore Skill Graph│
      └─────────┬─────────┘       └─────────┬─────────┘
                │                           │
                ▼                           ▼
      ┌───────────────────┐       ┌───────────────────┐
      │   Skill Gap       │       │ Prerequisites &   │
      │    Analysis       │       │ Related Skills    │
      └─────────┬─────────┘       └─────────┬─────────┘
                │                           │
                ▼                           ▼
      ┌───────────────────┐       ┌───────────────────┐
      │ Missing Skills +  │       │ Learning Paths +  │
      │ Resources         │       │ Related Careers   │
      └───────────────────┘       └───────────────────┘
```

---

## 🧩 Tech Stack

| Layer | Technology |
|---|---|
| 🎨 Frontend | React + Vite + Tailwind CSS |
| ⚙️ Backend | Python + FastAPI |
| 🗄️ Database | CognoDB (openCypher / Bolt) |
| 🔌 DB Driver | Official `neo4j` Python driver |
| ✅ Validation | Pydantic |
| 🚀 Frontend Deployment | Vercel |
| ☁️ Backend Deployment | Render |

---

## 🕸️ Graph Model

### Nodes

```text
User
Skill
Career
Resource
```

### Relationships

```text
User     -[:HAS_SKILL]->         Skill
Career   -[:REQUIRES]->          Skill
Skill    -[:RELATED_TO]->        Skill
Skill    -[:PREREQUISITE_FOR]->  Skill
Resource -[:TEACHES]->           Skill
```

### Conceptual Graph

```text
                         ┌────────────┐
                         │   Career   │
                         └─────┬──────┘
                               │ REQUIRES
                               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  Skill A │───▶│  Skill B │───▶│  Skill C │
        └────┬─────┘    └────┬─────┘    └────┬─────┘
             │ RELATED_TO      │                │
             ▼                 ▼                ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │  Skill D │     │ Resource │     │ Resource │
        └──────────┘     └──────────┘     └──────────┘
                              │
                              │ TEACHES
                              ▼
                            Skill

        ┌──────────┐
        │   User   │
        └────┬─────┘
             │ HAS_SKILL
             ▼
           Skill
```

### Example prerequisite chain

```text
Python
  ↓
Machine Learning
  ↓
Deep Learning
  ↓
NLP
  ↓
LLM Applications
```

This seeded chain demonstrates how SkillGraph can represent multi-hop learning dependencies. 

---

## 💡 Why a Graph Database?

Many of SkillGraph's most useful features are relationship-heavy.

For example, finding the skills required by a career is naturally represented as:

```cypher
MATCH (c:Career {id: $career_id})-[:REQUIRES]->(s:Skill)
WHERE NOT s.id IN $known_skill_ids
RETURN s.id AS id, s.name AS name, s.category AS category
```

And a multi-hop prerequisite path can be expressed as:

```cypher
MATCH (from:Skill {id: $from_id}), (to:Skill {id: $to_id})
MATCH path = shortestPath(
  (from)-[:PREREQUISITE_FOR*1..6]->(to)
)
RETURN
  [n IN nodes(path) | {id: n.id, name: n.name}] AS path_nodes,
  length(path) AS hop_count
```

This keeps the core domain logic focused on **relationships and traversals** rather than forcing everything into relational joins.

---

## 🛠️ Key Features

### 🎯 Career Explorer
Browse the available career roles and inspect the skills each career requires.

### 🧠 Skill Explorer
Explore individual skills together with their related and prerequisite neighbors.

### 📊 Skill Gap Analysis
Provide the skills you already know and a target career to identify:

```text
Your Skills
    +
Target Career
    ↓
Required Skills
    ↓
Set Difference
    ↓
Missing Skills
    ↓
Learning Resources
```

### 🧭 Learning Paths
Find a multi-hop prerequisite path between two skills.

Example:

```text
Python
  → Machine Learning
  → Deep Learning
  → NLP
  → LLM Applications
```

### 🔗 Related Careers
Discover other careers that overlap with a selected career through shared required skills.

### ❤️ Health Monitoring
The frontend can poll `/api/health` and display the current API/database availability state.

---

## 📡 API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | API + database health |
| `GET` | `/api/careers` | List all careers |
| `GET` | `/api/careers/{id}` | Career + required skills |
| `GET` | `/api/skills` | List all skills |
| `GET` | `/api/skills/{id}` | Skill + related/prerequisite neighbors |
| `POST` | `/api/skill-gap` | Calculate missing skills + resources |
| `GET` | `/api/learning-path` | Find prerequisite learning path |

All request bodies and parameters are validated with **Pydantic**, and Cypher values are passed using parameters such as `$career_id` rather than string concatenation.

---

## 🗂️ Repository Structure

```text
skillgraph/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── routers/
│   │   ├── services/
│   │   ├── queries/
│   │   └── schemas/
│   ├── scripts/
│   │   └── seed.py
│   ├── requirements.txt
│   ├── render.yaml
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── client.js
    │   ├── pages/
    │   │   ├── CareerExplorer
    │   │   ├── SkillExplorer
    │   │   └── GapAnalysis
    │   └── components/
    │       ├── NavBar
    │       ├── SkillChip
    │       ├── LoadingState
    │       ├── EmptyState
    │       └── ErrorState
    ├── vercel.json
    └── .env.example
```

---

## 💻 Run Locally

### 🗄️ Create and Configure the CognoDB Instance

SkillGraph uses **CognoDB** as its graph database through **openCypher over Bolt** and the official `neo4j` Python driver.

1. Create or sign in to your CognoDB account.
2. Create a new **database instance** for the SkillGraph project.
3. Obtain the instance's **Bolt connection URI** and database credentials.
4. Configure the backend environment file:

```env
NEO4J_URI=<your-cognodb-bolt-uri>
NEO4J_USER=<your-cognodb-username>
NEO4J_PASSWORD=<your-cognodb-password>
NEO4J_DATABASE=<your-cognodb-database-name>
```

5. Make sure the database instance is running and reachable from the backend environment.
6. Seed the graph:

```bash
cd backend
python scripts/seed.py
```

The seed script populates the careers, skills, resources, and graph relationships used by the application.

> **Security note:** Keep real credentials out of Git. Commit `.env.example`, not your production `.env`.


### 1. Clone the repository

```bash
git clone <your-repository-url>
cd skillgraph
```

### 2. Backend

```bash
cd backend

python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Then configure your real CognoDB connection values.

Seed the graph:

```bash
python scripts/seed.py
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/api/health
```

### 3. Frontend

```bash
cd frontend
npm install
```

Create the frontend environment file and point it to the local backend:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start Vite:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🖥️ UI Screenshots

The live application is available at **https://skillgraph-self.vercel.app/**.

Place the actual screenshots in `docs/screenshots/` using these filenames so GitHub renders them automatically.

### 🌐 Career Explorer

![SkillGraph Career Explorer](docs/screenshots/career-explorer.png)

Explore available career roles and inspect the skills required by each role.

### 🕸️ Skill Explorer / Relationship Graph

![SkillGraph Skill Explorer](docs/screenshots/skill-explorer.png)

Explore skills and their prerequisite and related-skill relationships.

### 📊 Skill Gap Analysis

![SkillGraph Skill Gap Analysis](docs/screenshots/skill-gap-analysis.png)

Select your existing skills, choose a target career, and view the missing skills and learning resources.

### 🧭 Learning Path

![SkillGraph Learning Path](docs/screenshots/learning-path.png)

Discover prerequisite paths between skills to turn a skill gap into an actionable learning sequence.

---

## ☁️ Production Deployment

### Frontend — Vercel

The frontend is deployed at:

**https://skillgraph-self.vercel.app/**

Set the Vercel environment variable:

```env
VITE_API_BASE_URL=https://skillgraph-0izb.onrender.com
```

Then redeploy the frontend so the Vite build picks up the updated value.

### Backend — Render

The backend is deployed at:

**https://skillgraph-0izb.onrender.com**

Configure the production database and CORS environment variables on Render.

Example:

```env
NEO4J_URI=<production-cognodb-uri>
NEO4J_USER=<production-user>
NEO4J_PASSWORD=<production-password>
NEO4J_DATABASE=<production-database>
ALLOWED_ORIGIN=https://skillgraph-self.vercel.app
```

> For temporary testing with local development, the allowed-origin configuration can include the local frontend origin as well.

Before first production use, seed the production graph:

```bash
python scripts/seed.py
```

Then verify:

```text
https://skillgraph-0izb.onrender.com/api/health
https://skillgraph-0izb.onrender.com/api/careers
https://skillgraph-0izb.onrender.com/api/skills
```

---

## 🛡️ Reliability & Failure Handling

SkillGraph is designed to fail cleanly when the database is unavailable.

- The Neo4j/CognoDB driver is created once during application startup.
- `verify_connectivity()` is checked during boot, but a failed check does not crash the API process.
- Database-specific router failures are caught and returned as a clean `503`.
- `/api/health` exposes live database status.
- The frontend can surface a connected/degraded state instead of showing an unexplained application failure.

Example degraded response behavior:

```text
Database unavailable
        ↓
FastAPI still starts
        ↓
/api/health → degraded
/api/careers → 503
        ↓
Frontend displays an actionable error state
```

---

## 🔐 Security & Design Notes

- Cypher inputs are parameterized using `$param` values.
- Variable-length prerequisite bounds are fixed at `1..6`; user-controlled IDs remain parameterized.
- The graph is currently **read-oriented** from the UI perspective.
- The current gap-analysis experience passes selected skill IDs directly in the request rather than persisting them to a logged-in `User` node.

---

## ⚠️ Known Simplifications

This version intentionally keeps the scope focused on graph traversal and career/skill exploration.

### No authentication yet

The `User` node and `HAS_SKILL` relationship exist in the graph model, but the UI currently does not persist a logged-in user's skills.

A future implementation could introduce:

```text
Login
  ↓
User profile
  ↓
Persist HAS_SKILL relationships
  ↓
Personalized skill graph
  ↓
Persistent career progress
```

### No caching layer

Requests currently reach CognoDB directly. This is suitable for the current data scale, while a production-scale implementation could add caching, background processing, or read optimization.

---

## 🧪 Useful API Test Commands

Health:

```bash
curl https://skillgraph-0izb.onrender.com/api/health
```

Careers:

```bash
curl https://skillgraph-0izb.onrender.com/api/careers
```

Skills:

```bash
curl https://skillgraph-0izb.onrender.com/api/skills
```

Interactive API documentation:

👉 https://skillgraph-0izb.onrender.com/docs

---

## ✅ Assignment Requirements Coverage

| Requirement | Covered |
|---|---|
| Use case | ✅ Career and skill relationship explorer + end-to-end user flow |
| Why a graph database? | ✅ Graph-native explanation and examples |
| Data model diagram | ✅ Nodes, relationships, and conceptual graph |
| Setup and run instructions | ✅ Backend and frontend local setup |
| Create the CognoDB instance | ✅ Dedicated CognoDB setup section |
| Main queries explained | ✅ Skill-gap, learning-path, and related-career Cypher |
| UI screenshots | ✅ Dedicated screenshot section |

## 🗺️ Future Roadmap

```text
✅ Career exploration
✅ Skill exploration
✅ Skill-gap analysis
✅ Prerequisite learning paths
✅ Related-career traversal
✅ Learning resources
✅ Production deployment

🔲 Authentication
🔲 Persistent user skill profiles
🔲 User-specific career recommendations
🔲 Visual graph canvas
🔲 Progress tracking
🔲 Skill mastery levels
🔲 Personalized learning plans
🔲 Caching / performance layer
```

---

## 🎓 Project Focus

SkillGraph demonstrates how a graph database can model a domain where **relationships are the product**, not just supporting data.

The central idea is simple:

> **A career is not just a list of skills — it is a connected dependency graph.**

That graph makes skill gaps, prerequisites, learning paths, and related careers natural traversal problems.

---

<p align="center">
  Built with React, FastAPI, CognoDB, openCypher, and a graph-first approach.
</p>

<p align="center">
  <a href="https://skillgraph-self.vercel.app/">🌐 Open SkillGraph</a>
  ·
  <a href="https://skillgraph-0izb.onrender.com/docs">📚 Explore API</a>
</p>
