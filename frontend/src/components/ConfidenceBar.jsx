/**
 * ConfidenceBar — progress bar horizontal untuk probabilitas prediksi.
 * Props:
 *   confidenceBullying: number (0-1)
 *   confidenceNonBullying: number (0-1)
 *   showLabels: boolean
 */
export default function ConfidenceBar({
  confidenceBullying = 0,
  confidenceNonBullying = 1,
  showLabels = true,
}) {
  const pctBully = Math.round(confidenceBullying * 100)
  const pctSafe = Math.round(confidenceNonBullying * 100)

  return (
    <div className="w-full space-y-2">
      {showLabels && (
        <div className="flex justify-between text-xs text-slate-400 mb-1">
          <span>Probabilitas Aman</span>
          <span>Probabilitas Bullying</span>
        </div>
      )}

      {/* Bar utama */}
      <div className="flex rounded-full overflow-hidden h-4 bg-slate-700">
        <div
          className="bg-emerald-500 transition-all duration-500 ease-out flex items-center justify-center"
          style={{ width: `${pctSafe}%` }}
        >
          {pctSafe >= 15 && (
            <span className="text-[10px] font-bold text-white">{pctSafe}%</span>
          )}
        </div>
        <div
          className="bg-red-500 transition-all duration-500 ease-out flex items-center justify-center"
          style={{ width: `${pctBully}%` }}
        >
          {pctBully >= 15 && (
            <span className="text-[10px] font-bold text-white">{pctBully}%</span>
          )}
        </div>
      </div>

      {/* Legend */}
      <div className="flex justify-between text-sm">
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block" />
          <span className="text-slate-300">Aman: <strong className="text-emerald-400">{pctSafe}%</strong></span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-red-500 inline-block" />
          <span className="text-slate-300">Bullying: <strong className="text-red-400">{pctBully}%</strong></span>
        </div>
      </div>
    </div>
  )
}
