export default function ErrorState({ message = "Something went wrong.", onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-xl border border-signal-amber/30 bg-signal-amber/5 py-14 text-center">
      <span className="text-2xl">⚠</span>
      <p className="max-w-sm text-sm text-mist-200">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="rounded-lg border border-signal-amber/40 px-4 py-1.5 text-sm text-signal-amber transition hover:bg-signal-amber/10"
        >
          Try again
        </button>
      )}
    </div>
  );
}
