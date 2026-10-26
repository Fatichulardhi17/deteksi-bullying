import { NavLink } from 'react-router-dom'
import { Shield, Brain, MessageSquare, BarChart2, AlertTriangle } from 'lucide-react'

const navItems = [
  { to: '/', label: 'Dashboard', icon: BarChart2, end: true },
  { to: '/predict', label: 'Prediksi Teks', icon: Brain },
  { to: '/conversation', label: 'Analisis Percakapan', icon: MessageSquare },
]

export default function Navbar() {
  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-slate-900 border-r border-slate-700/60 flex flex-col z-20">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-slate-700/60">
        <div className="relative">
          <div className="w-9 h-9 rounded-xl bg-violet-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-slate-900" />
        </div>
        <div>
          <h1 className="text-white font-bold text-sm leading-tight">BullyGuard</h1>
          <p className="text-slate-500 text-xs">Deteksi Bullying AI</p>
        </div>
      </div>

      {/* Nav links */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                isActive
                  ? 'bg-violet-600/20 text-violet-300 border border-violet-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`
            }
          >
            <Icon className="w-4 h-4 flex-shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-slate-700/60">
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <AlertTriangle className="w-3 h-3 text-amber-500" />
          <span>Hanya untuk edukasi</span>
        </div>
        <p className="text-xs text-slate-600 mt-1">Model: Logistic Regression</p>
      </div>
    </aside>
  )
}
