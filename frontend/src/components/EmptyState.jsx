export default function EmptyState({ title = "Nothing here yet", description, icon = "○" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-ink-600 py-14 text-center">
      <span className="text-2xl text-mist-400">{icon}</span>
      <p className="font-display text-base font-medium text-mist-200">{title}</p>
      {description && <p className="max-w-sm text-sm text-mist-400">{description}</p>}
    </div>
  );
}
