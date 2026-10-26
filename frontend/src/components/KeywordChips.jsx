/**
 * KeywordChips — chip/tag untuk kata kunci bullying yang terdeteksi.
 * Props:
 *   keywords: string[]
 */
export default function KeywordChips({ keywords = [] }) {
  if (!keywords || keywords.length === 0) {
    return (
      <div className="flex items-center gap-2 text-slate-500 text-sm">
        <span className="text-base">✅</span>
        <span>Tidak ada kata kunci bullying terdeteksi</span>
      </div>
    )
  }

  return (
    <div>
      <p className="text-xs text-slate-400 mb-2 flex items-center gap-1.5">
        <span className="text-amber-400">⚠️</span>
        {keywords.length} kata kunci terdeteksi:
      </p>
      <div className="flex flex-wrap gap-2">
        {keywords.map((kw, i) => (
          <span
            key={i}
            className="inline-flex items-center bg-red-500/15 border border-red-500/30 text-red-300 text-xs font-mono px-2.5 py-1 rounded-md"
          >
            {kw}
          </span>
        ))}
      </div>
    </div>
  )
}
