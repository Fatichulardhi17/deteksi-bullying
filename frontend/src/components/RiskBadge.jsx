/**
 * RiskBadge — badge berwarna berdasarkan level risiko.
 * Props:
 *   riskLevel: string — "🔴 Tinggi" | "🟡 Sedang" | "🟢 Rendah"
 *   label: int — 0 = aman, 1 = bullying
 *   size: "sm" | "md" | "lg"
 */
export default function RiskBadge({ riskLevel = '', label = 0, size = 'md' }) {
  const isHigh = riskLevel.includes('Tinggi')
  const isMid = riskLevel.includes('Sedang')
  const isLow = riskLevel.includes('Rendah')

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-1.5',
  }

  const colorClass = label === 1
    ? isHigh
      ? 'bg-red-500/20 text-red-400 border border-red-500/40'
      : 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
    : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'

  const icon = label === 1
    ? (isHigh ? '🔴' : '🟡')
    : '🟢'

  const text = label === 1
    ? (isHigh ? 'Risiko Tinggi' : 'Risiko Sedang')
    : 'Aman'

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-semibold ${sizeClasses[size]} ${colorClass}`}>
      <span>{icon}</span>
      <span>{text}</span>
    </span>
  )
}
