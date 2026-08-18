export default function LoadingState({ label = "Loading…" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 text-mist-400">
      <div className="relative h-8 w-8">
        <span className="absolute inset-0 rounded-full border-2 border-ink-600" />
        <span className="absolute inset-0 rounded-full border-2 border-t-signal-teal animate-spin" />
      </div>
      <p className="text-sm">{label}</p>
    </div>
  );
}
