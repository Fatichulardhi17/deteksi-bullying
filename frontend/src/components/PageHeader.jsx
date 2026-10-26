/**
 * PageHeader — header konsisten untuk setiap halaman.
 * Props:
 *   title: string
 *   description: string
 *   icon: Lucide icon component
 *   iconColor: string — Tailwind color class (default: "text-violet-400")
 */
export default function PageHeader({ title, description, icon: Icon, iconColor = 'text-violet-400' }) {
  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-2">
        {Icon && (
          <div className="w-9 h-9 rounded-lg bg-slate-700/60 flex items-center justify-center">
            <Icon className={`w-5 h-5 ${iconColor}`} />
          </div>
        )}
        <h2 className="text-2xl font-bold text-white">{title}</h2>
      </div>
      {description && (
        <p className="text-slate-400 text-sm ml-12">{description}</p>
      )}
    </div>
  )
}
