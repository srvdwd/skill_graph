import { useEffect, useState } from "react";
import { api, ApiError } from "../api/client";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import SkillChip from "../components/SkillChip";

export default function GapAnalysis() {
  const [skills, setSkills] = useState(null);
  const [careers, setCareers] = useState(null);
  const [loadError, setLoadError] = useState(null);

  const [knownIds, setKnownIds] = useState(new Set());
  const [targetCareerId, setTargetCareerId] = useState("");

  const [result, setResult] = useState(null);
  const [resultError, setResultError] = useState(null);
  const [resultLoading, setResultLoading] = useState(false);

  function loadOptions() {
    setLoadError(null);
    setSkills(null);
    setCareers(null);
    Promise.all([api.getSkills(), api.getCareers()])
      .then(([s, c]) => {
        setSkills(s);
        setCareers(c);
      })
      .catch((err) => setLoadError(err instanceof ApiError ? err.message : "Unexpected error"));
  }

  useEffect(loadOptions, []);

  function toggleSkill(id) {
    setKnownIds((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  function runAnalysis() {
    if (!targetCareerId) return;
    setResult(null);
    setResultError(null);
    setResultLoading(true);
    api
      .postSkillGap({ known_skill_ids: Array.from(knownIds), target_career_id: targetCareerId })
      .then(setResult)
      .catch((err) => setResultError(err instanceof ApiError ? err.message : "Unexpected error"))
      .finally(() => setResultLoading(false));
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h2 className="mb-1 font-display text-2xl font-semibold text-mist-100">Skill gap analysis</h2>
        <p className="text-sm text-mist-400">
          Select the skills you already have, choose a target career, and see exactly what's missing —
          along with resources to learn it.
        </p>
      </div>

      {loadError && <ErrorState message={loadError} onRetry={loadOptions} />}

      {!loadError && (skills === null || careers === null) && <LoadingState label="Loading skills and careers…" />}

      {!loadError && skills && careers && (
        <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <section className="rounded-xl border border-ink-700 bg-ink-900 p-5">
            <p className="mb-3 text-xs font-medium uppercase tracking-wide text-mist-400">
              1. Your existing skills ({knownIds.size} selected)
            </p>
            {skills.length === 0 ? (
              <EmptyState title="No skills available" />
            ) : (
              <div className="flex max-h-72 flex-wrap gap-2 overflow-y-auto pr-1">
                {skills.map((skill) => (
                  <SkillChip
                    key={skill.id}
                    label={skill.name}
                    selected={knownIds.has(skill.id)}
                    onClick={() => toggleSkill(skill.id)}
                  />
                ))}
              </div>
            )}

            <p className="mb-2 mt-6 text-xs font-medium uppercase tracking-wide text-mist-400">
              2. Target career
            </p>
            {careers.length === 0 ? (
              <EmptyState title="No careers available" />
            ) : (
              <select
                value={targetCareerId}
                onChange={(e) => setTargetCareerId(e.target.value)}
                className="w-full rounded-lg border border-ink-600 bg-ink-800 px-3 py-2 text-sm text-mist-100"
              >
                <option value="">Select a career…</option>
                {careers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.title}
                  </option>
                ))}
              </select>
            )}

            <button
              onClick={runAnalysis}
              disabled={!targetCareerId}
              className="mt-5 w-full rounded-lg bg-signal-teal px-4 py-2.5 text-sm font-semibold text-ink-950 transition hover:opacity-90 disabled:opacity-40"
            >
              Analyze skill gap
            </button>
          </section>

          <section className="rounded-xl border border-ink-700 bg-ink-900 p-5">
            <p className="mb-3 text-xs font-medium uppercase tracking-wide text-mist-400">3. Results</p>

            {!result && !resultLoading && !resultError && (
              <EmptyState icon="◎" title="Run an analysis" description="Your results will appear here." />
            )}
            {resultLoading && <LoadingState label="Analyzing skill gap…" />}
            {resultError && <ErrorState message={resultError} onRetry={runAnalysis} />}

            {result && !resultLoading && (
              <div>
                <p className="font-display text-lg font-semibold text-mist-100">{result.target_career_title}</p>
                <p className="mb-4 text-sm text-mist-400">
                  {result.known_skill_count} of {result.required_skill_count} required skills known
                </p>

                {result.missing_skills.length === 0 ? (
                  <EmptyState
                    icon="✓"
                    title="No gap!"
                    description="You already have every skill required for this career."
                  />
                ) : (
                  <div className="flex flex-col gap-3">
                    {result.missing_skills.map((skill) => (
                      <div key={skill.id} className="rounded-lg border border-signal-amber/25 bg-signal-amber/5 p-3">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-mist-100">{skill.name}</p>
                          <span className="text-xs text-mist-400">{skill.category}</span>
                        </div>
                        {skill.resources.length > 0 ? (
                          <ul className="mt-2 flex flex-col gap-1">
                            {skill.resources.map((r) => (
                              <li key={r.id}>
                                <a
                                  href={r.url}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="text-xs text-signal-teal hover:underline"
                                >
                                  {r.title} · {r.type}
                                </a>
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <p className="mt-2 text-xs text-mist-400">No resources linked yet.</p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  );
}
