import { useEffect, useState } from "react";
import { api, ApiError } from "../api/client";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import SkillChip from "../components/SkillChip";

export default function SkillExplorer() {
  const [skills, setSkills] = useState(null);
  const [error, setError] = useState(null);

  const [selectedId, setSelectedId] = useState(null);
  const [detail, setDetail] = useState(null);
  const [detailError, setDetailError] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const [fromSkill, setFromSkill] = useState("");
  const [toSkill, setToSkill] = useState("");
  const [path, setPath] = useState(null);
  const [pathError, setPathError] = useState(null);
  const [pathLoading, setPathLoading] = useState(false);

  function loadSkills() {
    setError(null);
    setSkills(null);
    api
      .getSkills()
      .then(setSkills)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Unexpected error"));
  }

  useEffect(loadSkills, []);

  useEffect(() => {
    if (!selectedId) return;
    setDetail(null);
    setDetailError(null);
    setDetailLoading(true);
    api
      .getSkill(selectedId)
      .then(setDetail)
      .catch((err) => setDetailError(err instanceof ApiError ? err.message : "Unexpected error"))
      .finally(() => setDetailLoading(false));
  }, [selectedId]);

  function runPathSearch(e) {
    e.preventDefault();
    if (!fromSkill || !toSkill) return;
    setPath(null);
    setPathError(null);
    setPathLoading(true);
    api
      .getLearningPath(fromSkill, toSkill)
      .then(setPath)
      .catch((err) => setPathError(err instanceof ApiError ? err.message : "Unexpected error"))
      .finally(() => setPathLoading(false));
  }

  return (
    <div className="flex flex-col gap-8">
      <div className="grid gap-6 md:grid-cols-[1.1fr_1fr]">
        <section>
          <h2 className="mb-1 font-display text-xl font-semibold text-mist-100">Skills</h2>
          <p className="mb-4 text-sm text-mist-400">Browse skills and their prerequisite relationships.</p>

          {error && <ErrorState message={error} onRetry={loadSkills} />}
          {!error && skills === null && <LoadingState label="Loading skills…" />}
          {!error && skills !== null && skills.length === 0 && (
            <EmptyState title="No skills found" description="The graph doesn't contain any Skill nodes yet." />
          )}

          {!error && skills && skills.length > 0 && (
            <div className="flex max-h-96 flex-col gap-1 overflow-y-auto pr-1">
              {skills.map((skill) => (
                <button
                  key={skill.id}
                  onClick={() => setSelectedId(skill.id)}
                  className={`rounded-lg border px-3 py-2 text-left text-sm transition ${
                    selectedId === skill.id
                      ? "border-signal-teal bg-signal-teal/5 text-mist-100"
                      : "border-transparent text-mist-300 hover:bg-ink-800"
                  }`}
                >
                  <span className="font-medium">{skill.name}</span>
                  <span className="ml-2 text-xs text-mist-400">{skill.category}</span>
                </button>
              ))}
            </div>
          )}
        </section>

        <section className="rounded-xl border border-ink-700 bg-ink-900 p-5">
          {!selectedId && (
            <EmptyState icon="→" title="Select a skill" description="Choose a skill on the left to see its connections." />
          )}
          {selectedId && detailLoading && <LoadingState label="Loading skill details…" />}
          {selectedId && detailError && (
            <ErrorState message={detailError} onRetry={() => setSelectedId(selectedId)} />
          )}

          {selectedId && detail && !detailLoading && (
            <div>
              <h3 className="font-display text-lg font-semibold text-mist-100">{detail.name}</h3>
              <p className="mt-1 text-sm text-mist-400">{detail.description}</p>

              <p className="mb-2 mt-5 text-xs font-medium uppercase tracking-wide text-mist-400">
                Related skills ({detail.related_skills.length})
              </p>
              {detail.related_skills.length === 0 ? (
                <EmptyState title="No connections yet" />
              ) : (
                <div className="flex flex-wrap gap-2">
                  {detail.related_skills.map((rel) => (
                    <SkillChip
                      key={`${rel.id}-${rel.relationship}`}
                      label={`${rel.name} · ${rel.relationship === "PREREQUISITE_FOR" ? "prerequisite" : "related"}`}
                      tone={rel.relationship === "PREREQUISITE_FOR" ? "path" : "default"}
                    />
                  ))}
                </div>
              )}
            </div>
          )}
        </section>
      </div>

      <section className="rounded-xl border border-ink-700 bg-ink-900 p-5">
        <h2 className="mb-1 font-display text-xl font-semibold text-mist-100">Learning path finder</h2>
        <p className="mb-4 text-sm text-mist-400">
          Finds the shortest chain of prerequisite skills between two skills — a multi-hop graph traversal.
        </p>

        <form onSubmit={runPathSearch} className="flex flex-wrap items-end gap-3">
          <div className="flex flex-col gap-1">
            <label className="text-xs text-mist-400">From skill</label>
            <select
              value={fromSkill}
              onChange={(e) => setFromSkill(e.target.value)}
              className="rounded-lg border border-ink-600 bg-ink-800 px-3 py-2 text-sm text-mist-100"
            >
              <option value="">Select…</option>
              {skills?.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs text-mist-400">To skill</label>
            <select
              value={toSkill}
              onChange={(e) => setToSkill(e.target.value)}
              className="rounded-lg border border-ink-600 bg-ink-800 px-3 py-2 text-sm text-mist-100"
            >
              <option value="">Select…</option>
              {skills?.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>
          <button
            type="submit"
            disabled={!fromSkill || !toSkill}
            className="rounded-lg bg-signal-violet px-4 py-2 text-sm font-medium text-ink-950 transition hover:opacity-90 disabled:opacity-40"
          >
            Find path
          </button>
        </form>

        <div className="mt-5">
          {pathLoading && <LoadingState label="Searching for a path…" />}
          {pathError && <ErrorState message={pathError} onRetry={runPathSearch} />}
          {path && !pathLoading && !path.path_found && (
            <EmptyState
              icon="✕"
              title="No path found"
              description="There is no chain of prerequisite relationships connecting these two skills."
            />
          )}
          {path && !pathLoading && path.path_found && (
            <div className="flex flex-wrap items-center gap-2">
              {path.path.map((step, i) => (
                <div key={step.id} className="flex items-center gap-2">
                  <SkillChip label={step.name} tone="path" />
                  {i < path.path.length - 1 && <span className="text-mist-400">→</span>}
                </div>
              ))}
              <span className="ml-2 text-xs text-mist-400">({path.hop_count} hops)</span>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
