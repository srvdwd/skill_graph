const TABS = [
  { id: "careers", label: "Careers" },
  { id: "skills", label: "Skills" },
  { id: "gap", label: "Gap Analysis" },
];

export default function NavBar({ active, onNavigate, dbStatus }) {
  return (
    <header className="sticky top-0 z-10 border-b border-ink-700 bg-ink-950/85 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2">
          <span className="grid h-7 w-7 place-items-center rounded-md bg-gradient-to-br from-signal-violet to-signal-teal text-xs font-bold text-ink-950">
            SG
          </span>
          <span className="font-display text-sm font-semibold tracking-wide text-mist-100">
            SkillGraph
          </span>
        </div>

        <nav className="flex items-center gap-1 rounded-full border border-ink-700 bg-ink-900 p-1">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onNavigate(tab.id)}
              className={`rounded-full px-4 py-1.5 text-sm transition ${
                active === tab.id
                  ? "bg-signal-teal text-ink-950 font-medium"
                  : "text-mist-400 hover:text-mist-100"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        <div className="flex items-center gap-2 text-xs text-mist-400">
          <span
            className={`h-2 w-2 rounded-full ${
              dbStatus === "ok"
                ? "bg-signal-teal"
                : dbStatus === "degraded"
                ? "bg-signal-amber"
                : "bg-ink-600"
            }`}
          />
          {dbStatus === "ok" ? "DB connected" : dbStatus === "degraded" ? "DB unavailable" : "Checking…"}
        </div>
      </div>
    </header>
  );
}
