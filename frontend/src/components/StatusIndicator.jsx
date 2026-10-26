import { useEffect, useState } from 'react'
import { getHealth } from '../services/api'
import { Wifi, WifiOff } from 'lucide-react'

export default function StatusIndicator() {
  const [status, setStatus] = useState('checking') // checking | ok | error

  useEffect(() => {
    const check = async () => {
      try {
        const data = await getHealth()
        setStatus(data.model_ready ? 'ok' : 'error')
      } catch {
        setStatus('error')
      }
    }
    check()
    const interval = setInterval(check, 30000)
    return () => clearInterval(interval)
  }, [])

  if (status === 'checking') {
    return (
      <div className="flex items-center gap-1.5 text-xs text-slate-500">
        <span className="w-1.5 h-1.5 rounded-full bg-slate-500 animate-pulse" />
        Menghubungkan...
      </div>
    )
  }

  if (status === 'error') {
    return (
      <div className="flex items-center gap-1.5 text-xs text-red-400">
        <WifiOff className="w-3 h-3" />
        Backend offline
      </div>
    )
  }

  return (
    <div className="flex items-center gap-1.5 text-xs text-emerald-400">
      <Wifi className="w-3 h-3" />
      Model aktif
    </div>
  )
}
