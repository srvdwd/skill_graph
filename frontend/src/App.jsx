import { useEffect, useState } from "react";
import { api } from "./api/client";
import NavBar from "./components/NavBar";
import CareerExplorer from "./pages/CareerExplorer";
import SkillExplorer from "./pages/SkillExplorer";
import GapAnalysis from "./pages/GapAnalysis";

export default function App() {
  const [page, setPage] = useState("gap");
  const [dbStatus, setDbStatus] = useState("checking");

  useEffect(() => {
    function poll() {
      api
        .getHealth()
        .then((res) => setDbStatus(res.database_connected ? "ok" : "degraded"))
        .catch(() => setDbStatus("degraded"));
    }
    poll();
    const interval = setInterval(poll, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen">
      <NavBar active={page} onNavigate={setPage} dbStatus={dbStatus} />

      <main className="mx-auto max-w-5xl px-6 py-10">
        {page === "gap" && (
          <div className="mb-10">
            <p className="mb-2 text-xs font-medium uppercase tracking-widest text-signal-violet">
              Career &amp; skill relationship explorer
            </p>
            <h1 className="max-w-2xl font-display text-3xl font-semibold leading-tight text-mist-100 sm:text-4xl">
              See exactly which skills stand between you and your next role.
            </h1>
            <p className="mt-3 max-w-xl text-sm text-mist-400">
              SkillGraph models careers, skills, and their prerequisites as a connected graph —
              so gap analysis, learning paths, and related roles fall out as simple traversals,
              not brittle joins.
            </p>
          </div>
        )}

        {page === "careers" && <CareerExplorer />}
        {page === "skills" && <SkillExplorer />}
        {page === "gap" && <GapAnalysis />}
      </main>

      <footer className="mx-auto max-w-5xl px-6 pb-10 pt-4 text-xs text-mist-400">
        SkillGraph · Backed by CognoDB (openCypher over Bolt)
      </footer>
    </div>
  );
}
