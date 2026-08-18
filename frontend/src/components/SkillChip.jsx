export default function SkillChip({ label, selected, onClick, tone = "default" }) {
  const toneClasses = {
    default: selected
      ? "bg-signal-teal text-ink-950 border-signal-teal"
      : "bg-ink-800 text-mist-200 border-ink-600 hover:border-signal-teal/60",
    missing: "bg-signal-amber/10 text-signal-amber border-signal-amber/30",
    path: "bg-signal-violet/10 text-signal-violet border-signal-violet/30",
  };

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={!onClick}
      className={`rounded-full border px-3 py-1.5 text-xs font-medium transition ${toneClasses[tone]} ${
        onClick ? "cursor-pointer" : "cursor-default"
      }`}
    >
      {label}
    </button>
  );
}
