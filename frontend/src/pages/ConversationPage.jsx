import { useState } from 'react'
import { MessageSquare, Plus, Trash2, Send, RotateCcw, User, AlertCircle } from 'lucide-react'
import PageHeader from '../components/PageHeader'
import RiskBadge from '../components/RiskBadge'
import ConfidenceBar from '../components/ConfidenceBar'
import KeywordChips from '../components/KeywordChips'
import { analyzeConversation } from '../services/api'

const CONTOH_PERCAKAPAN = [
  { sender: 'Budi', text: 'hei, lo tuh bego banget sih!' },
  { sender: 'Siti', text: 'aku ga ngerti maksudmu' },
  { sender: 'Budi', text: 'dasar tolol, malu-maluin aja' },
  { sender: 'Siti', text: 'tolong jangan kasar dong' },
  { sender: 'Andi', text: 'udah, kalian berdamai aja yuk' },
  { sender: 'Budi', text: 'awas lo ya, besok ketemu gue hajar' },
]

export default function ConversationPage() {
  const [messages, setMessages] = useState([
    { sender: '', text: '' },
  ])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const addMessage = () => {
    setMessages([...messages, { sender: '', text: '' }])
  }

  const removeMessage = (i) => {
    if (messages.length === 1) return
    setMessages(messages.filter((_, idx) => idx !== i))
  }

  const updateMessage = (i, field, value) => {
    const updated = [...messages]
    updated[i] = { ...updated[i], [field]: value }
    setMessages(updated)
  }

  const loadContoh = () => {
    setMessages(CONTOH_PERCAKAPAN.map(m => ({ ...m })))
    setResult(null)
    setError(null)
  }

  const handleReset = () => {
    setMessages([{ sender: '', text: '' }])
    setResult(null)
    setError(null)
  }

  const handleAnalyze = async () => {
    const valid = messages.filter(m => m.text.trim())
    if (valid.length === 0) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeConversation(
        valid.map(m => ({
          sender: m.sender.trim() || 'Anonim',
          text: m.text.trim(),
        }))
      )
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const validCount = messages.filter(m => m.text.trim()).length

  return (
    <div className="max-w-3xl mx-auto fade-in">
      <PageHeader
        title="Analisis Percakapan"
        description="Masukkan rangkaian pesan untuk mendeteksi pola bullying dalam percakapan."
        icon={MessageSquare}
        iconColor="text-blue-400"
      />

      {/* Input form */}
      <div className="card mb-6">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm font-medium text-slate-300">
            Pesan ({validCount} valid)
          </p>
          <button
            onClick={loadContoh}
            className="text-xs text-violet-400 hover:text-violet-300 border border-violet-500/30 hover:border-violet-400/50 px-3 py-1 rounded-md transition-colors"
          >
            Muat Contoh
          </button>
        </div>

        <div className="space-y-3 max-h-[400px] overflow-y-auto pr-1">
          {messages.map((msg, i) => (
            <div key={i} className="flex gap-2 items-start">
              <span className="text-slate-600 text-xs w-5 pt-3 flex-shrink-0 text-right">{i + 1}</span>
              <input
                className="input-field w-28 flex-shrink-0 text-sm"
                placeholder="Pengirim"
                value={msg.sender}
                onChange={(e) => updateMessage(i, 'sender', e.target.value)}
              />
              <input
                className="input-field flex-1 text-sm"
                placeholder="Teks pesan..."
                value={msg.text}
                onChange={(e) => updateMessage(i, 'text', e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    if (i === messages.length - 1) addMessage()
                  }
                }}
              />
              <button
                onClick={() => removeMessage(i)}
                className="p-2.5 text-slate-600 hover:text-red-400 transition-colors flex-shrink-0"
                disabled={messages.length === 1}
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>

        <button
          onClick={addMessage}
          className="mt-3 flex items-center gap-2 text-sm text-slate-400 hover:text-violet-400 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Tambah pesan
        </button>

        <div className="flex gap-3 mt-5">
          <button
            className="btn-primary flex items-center gap-2 flex-1 justify-center"
            onClick={handleAnalyze}
            disabled={loading || validCount === 0}
          >
            {loading ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Menganalisis...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Analisis Percakapan
              </>
            )}
          </button>
          <button className="btn-secondary flex items-center gap-2" onClick={handleReset}>
            <RotateCcw className="w-4 h-4" />
            Reset
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="card border-red-500/30 bg-red-500/5 mb-6">
          <p className="text-red-400 text-sm flex items-center gap-2">
            <AlertCircle className="w-4 h-4" /> {error}
          </p>
        </div>
      )}

      {/* Hasil analisis */}
      {result && (
        <div className="space-y-6 fade-in">
          {/* Summary cards */}
          <div className="grid grid-cols-3 gap-4">
            <div className="card text-center">
              <p className="text-3xl font-bold text-white">{result.total_pesan}</p>
              <p className="text-slate-400 text-xs mt-1">Total Pesan</p>
            </div>
            <div className={`card text-center ${result.total_bullying > 0 ? 'border-red-500/30' : 'border-emerald-500/30'}`}>
              <p className={`text-3xl font-bold ${result.total_bullying > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
                {result.total_bullying}
              </p>
              <p className="text-slate-400 text-xs mt-1">Pesan Bullying</p>
            </div>
            <div className="card text-center">
              <p className={`text-3xl font-bold ${result.bullying_ratio > 0.3 ? 'text-red-400' : result.bullying_ratio > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
                {(result.bullying_ratio * 100).toFixed(0)}%
              </p>
              <p className="text-slate-400 text-xs mt-1">Rasio Bullying</p>
            </div>
          </div>

          {/* Status keseluruhan */}
          <div className={`card flex items-center gap-4 ${result.total_bullying > 0 ? 'border-red-500/30 bg-red-500/5' : 'border-emerald-500/30 bg-emerald-500/5'}`}>
            <span className="text-3xl">{result.total_bullying > 0 ? '⚠️' : '✅'}</span>
            <div>
              <p className={`font-bold text-lg ${result.total_bullying > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
                {result.total_bullying > 0 ? 'Percakapan Berisiko' : 'Percakapan Aman'}
              </p>
              <p className="text-sm text-slate-400">
                {result.total_bullying > 0
                  ? `${result.total_bullying} pesan berindikasi bullying terdeteksi dalam percakapan ini.`
                  : 'Tidak ada indikasi bullying dalam percakapan ini.'}
              </p>
            </div>
          </div>

          {/* Statistik per pengirim */}
          {Object.keys(result.sender_stats).length > 0 && (
            <div className="card">
              <p className="section-title flex items-center gap-2">
                <User className="w-5 h-5 text-blue-400" />
                Statistik per Pengirim
              </p>
              <div className="space-y-3">
                {Object.entries(result.sender_stats).map(([sender, stats]) => (
                  <div key={sender} className="bg-slate-900 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-sm font-bold text-slate-300">
                          {sender[0]?.toUpperCase()}
                        </div>
                        <span className="font-medium text-slate-200">{sender}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-slate-400">
                        <span>{stats.pesan_bullying}/{stats.total_pesan} bullying</span>
                        {stats.pesan_bullying > 0 && (
                          <span className="bg-red-500/20 text-red-400 text-xs px-2 py-0.5 rounded-full border border-red-500/30">
                            ⚠️ Terindikasi
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-500">
                      <span>Avg. risk score: <strong className={stats.avg_risk_score > 0.5 ? 'text-red-400' : stats.avg_risk_score > 0.3 ? 'text-amber-400' : 'text-emerald-400'}>
                        {(stats.avg_risk_score * 100).toFixed(1)}%
                      </strong></span>
                    </div>
                    {/* Mini bar */}
                    <div className="mt-2 h-1.5 rounded-full bg-slate-700 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${stats.avg_risk_score > 0.5 ? 'bg-red-500' : stats.avg_risk_score > 0.3 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                        style={{ width: `${stats.avg_risk_score * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Timeline pesan dengan prediksi */}
          {result.detailed_messages && (
            <div className="card">
              <p className="section-title flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-violet-400" />
                Detail Pesan
              </p>
              <div className="space-y-2">
                {result.detailed_messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`rounded-lg p-3 border ${
                      msg.prediction.label === 1
                        ? 'bg-red-500/8 border-red-500/25'
                        : 'bg-slate-900 border-slate-700/50'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2 mb-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-slate-500 w-4">{i + 1}.</span>
                        <span className="text-sm font-medium text-slate-300">{msg.sender}</span>
                      </div>
                      <RiskBadge riskLevel={msg.prediction.risk_level} label={msg.prediction.label} size="sm" />
                    </div>
                    <p className="text-sm text-slate-200 ml-6">{msg.text}</p>
                    {msg.prediction.detected_keywords.length > 0 && (
                      <div className="ml-6 mt-2">
                        <KeywordChips keywords={msg.prediction.detected_keywords} />
                      </div>
                    )}
                    <div className="ml-6 mt-2">
                      <ConfidenceBar
                        confidenceBullying={msg.prediction.confidence_bullying}
                        confidenceNonBullying={msg.prediction.confidence_non_bullying}
                        showLabels={false}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
