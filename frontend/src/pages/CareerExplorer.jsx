import { useEffect, useState } from "react";
import { api, ApiError } from "../api/client";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import SkillChip from "../components/SkillChip";

export default function CareerExplorer() {
  const [careers, setCareers] = useState(null);
  const [error, setError] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [detail, setDetail] = useState(null);
  const [detailError, setDetailError] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  function loadCareers() {
    setError(null);
    setCareers(null);
    api
      .getCareers()
      .then(setCareers)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Unexpected error"));
  }

  useEffect(loadCareers, []);

  useEffect(() => {
    if (!selectedId) return;
    setDetail(null);
    setDetailError(null);
    setDetailLoading(true);
    api
      .getCareer(selectedId)
      .then(setDetail)
      .catch((err) => setDetailError(err instanceof ApiError ? err.message : "Unexpected error"))
      .finally(() => setDetailLoading(false));
  }, [selectedId]);

  return (
    <div className="grid gap-6 md:grid-cols-[1.1fr_1fr]">
      <section>
        <h2 className="mb-1 font-display text-xl font-semibold text-mist-100">Career roles</h2>
        <p className="mb-4 text-sm text-mist-400">Pick a role to see the skills it requires.</p>

        {error && <ErrorState message={error} onRetry={loadCareers} />}
        {!error && careers === null && <LoadingState label="Loading careers…" />}
        {!error && careers !== null && careers.length === 0 && (
          <EmptyState title="No careers found" description="The graph doesn't contain any Career nodes yet." />
        )}

        {!error && careers && careers.length > 0 && (
          <ul className="flex flex-col gap-2">
            {careers.map((career) => (
              <li key={career.id}>
                <button
                  onClick={() => setSelectedId(career.id)}
                  className={`w-full rounded-xl border px-4 py-3 text-left transition ${
                    selectedId === career.id
                      ? "border-signal-teal bg-signal-teal/5"
                      : "border-ink-700 bg-ink-900 hover:border-ink-600"
                  }`}
                >
                  <p className="font-display font-medium text-mist-100">{career.title}</p>
                  <p className="mt-0.5 text-sm text-mist-400">{career.description}</p>
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="rounded-xl border border-ink-700 bg-ink-900 p-5">
        {!selectedId && (
          <EmptyState
            icon="→"
            title="Select a career"
            description="Choose a role on the left to see its required skills here."
          />
        )}

        {selectedId && detailLoading && <LoadingState label="Loading role details…" />}
        {selectedId && detailError && <ErrorState message={detailError} onRetry={() => setSelectedId(selectedId)} />}

        {selectedId && detail && !detailLoading && (
          <div>
            <h3 className="font-display text-lg font-semibold text-mist-100">{detail.title}</h3>
            <p className="mt-1 text-sm text-mist-400">{detail.description}</p>

            <p className="mb-2 mt-5 text-xs font-medium uppercase tracking-wide text-mist-400">
              Required skills ({detail.required_skills.length})
            </p>
            {detail.required_skills.length === 0 ? (
              <EmptyState title="No skills linked" description="This career has no REQUIRES relationships yet." />
            ) : (
              <div className="flex flex-wrap gap-2">
                {detail.required_skills.map((skill) => (
                  <SkillChip key={skill.id} label={skill.name} />
                ))}
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
