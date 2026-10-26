import { useState } from 'react'
import { Brain, Send, RotateCcw, ChevronDown, ChevronUp } from 'lucide-react'
import PageHeader from '../components/PageHeader'
import RiskBadge from '../components/RiskBadge'
import ConfidenceBar from '../components/ConfidenceBar'
import KeywordChips from '../components/KeywordChips'
import { predictText } from '../services/api'

const CONTOH = [
  'dasar goblok, ga bisa ngerjain soal gampang aja',
  'semangat ya ujiannya, pasti bisa kok!',
  'awas lo ya, besok gue hajar habis-habisan!',
  'kita belajar bareng yuk buat persiapan ujian',
  'lo tuh ga ada gunanya, semua orang benci sama lo',
  'makasih udah bantuin aku tadi, baik banget',
]

export default function PredictPage() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showLexical, setShowLexical] = useState(false)

  const handlePredict = async () => {
    if (!text.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await predictText(text)
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setText('')
    setResult(null)
    setError(null)
  }

  const handleContoh = (t) => {
    setText(t)
    setResult(null)
    setError(null)
  }

  return (
    <div className="max-w-2xl mx-auto fade-in">
      <PageHeader
        title="Prediksi Teks"
        description="Masukkan satu teks chat untuk dianalisis model deteksi bullying."
        icon={Brain}
      />

      {/* Input area */}
      <div className="card mb-6">
        <label className="label">Teks yang ingin dianalisis</label>
        <textarea
          className="textarea-field"
          rows={4}
          placeholder="Ketik atau tempel teks chat di sini..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.ctrlKey && e.key === 'Enter') handlePredict()
          }}
        />
        <p className="text-xs text-slate-500 mt-1.5">Tekan Ctrl + Enter untuk prediksi cepat</p>

        {/* Contoh teks */}
        <div className="mt-4">
          <p className="label">Contoh teks:</p>
          <div className="flex flex-wrap gap-2">
            {CONTOH.map((t, i) => (
              <button
                key={i}
                onClick={() => handleContoh(t)}
                className="text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 px-2.5 py-1 rounded-md transition-colors duration-150 text-left"
                title={t}
              >
                {t.length > 30 ? t.slice(0, 30) + '…' : t}
              </button>
            ))}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex gap-3 mt-5">
          <button
            className="btn-primary flex items-center gap-2 flex-1 justify-center"
            onClick={handlePredict}
            disabled={loading || !text.trim()}
          >
            {loading ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Menganalisis...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Prediksi
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
            <span>⚠️</span> {error}
          </p>
        </div>
      )}

      {/* Hasil prediksi */}
      {result && (
        <div className="card fade-in space-y-6">
          {/* Status utama */}
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <p className="text-xs text-slate-400 mb-1">Teks yang dianalisis:</p>
              <p className="text-slate-200 text-sm bg-slate-900 rounded-lg px-3 py-2 border border-slate-700">
                &ldquo;{result.text_original}&rdquo;
              </p>
            </div>
            <RiskBadge riskLevel={result.risk_level} label={result.label} size="lg" />
          </div>

          {/* Prediksi label */}
          <div className={`rounded-xl p-4 flex items-center gap-4 ${
            result.label === 1
              ? 'bg-red-500/10 border border-red-500/25'
              : 'bg-emerald-500/10 border border-emerald-500/25'
          }`}>
            <span className="text-3xl">
              {result.label === 1 ? '⚠️' : '✅'}
            </span>
            <div>
              <p className={`text-lg font-bold ${result.label === 1 ? 'text-red-400' : 'text-emerald-400'}`}>
                {result.label === 1 ? 'Terdeteksi Bullying' : 'Tidak Ada Bullying'}
              </p>
              {result.warning_message && (
                <p className="text-amber-300 text-sm mt-0.5">{result.warning_message}</p>
              )}
            </div>
          </div>

          {/* Confidence bar */}
          <div>
            <p className="label">Distribusi Probabilitas</p>
            <ConfidenceBar
              confidenceBullying={result.confidence_bullying}
              confidenceNonBullying={result.confidence_non_bullying}
            />
          </div>

          {/* Keywords */}
          <div>
            <p className="label">Kata Kunci Terdeteksi</p>
            <KeywordChips keywords={result.detected_keywords} />
          </div>

          {/* Lexical features (accordion) */}
          {result.lexical_features && Object.keys(result.lexical_features).length > 0 && (
            <div>
              <button
                className="flex items-center gap-2 text-sm text-slate-400 hover:text-slate-200 transition-colors"
                onClick={() => setShowLexical(!showLexical)}
              >
                {showLexical ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                Fitur Leksikal ({Object.keys(result.lexical_features).length} fitur aktif)
              </button>
              {showLexical && (
                <div className="mt-3 grid grid-cols-2 gap-2 fade-in">
                  {Object.entries(result.lexical_features).map(([key, val]) => (
                    <div key={key} className="bg-slate-900 rounded-lg px-3 py-2 flex justify-between text-xs">
                      <span className="text-slate-400 font-mono">{key}</span>
                      <span className="text-violet-400 font-semibold">{typeof val === 'number' ? val.toFixed(3) : val}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Teks yang diproses */}
          <div>
            <p className="label">Teks setelah preprocessing</p>
            <p className="font-mono text-xs text-slate-400 bg-slate-900 rounded-lg px-3 py-2 border border-slate-700/50">
              {result.text_processed || <em className="text-slate-600">kosong setelah preprocessing</em>}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
