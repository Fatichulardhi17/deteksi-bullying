import { useState, useEffect } from 'react'
import { BarChart2, Shield, TrendingUp, AlertTriangle, CheckCircle, Send } from 'lucide-react'
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from 'recharts'
import PageHeader from '../components/PageHeader'
import RiskBadge from '../components/RiskBadge'
import ConfidenceBar from '../components/ConfidenceBar'
import { predictBatch, getHealth } from '../services/api'

const DEMO_TEXTS = [
  'dasar goblok, ga bisa ngerjain soal gampang aja',
  'semangat ya ujiannya, pasti bisa kok!',
  'awas lo ya, besok gue hajar habis-habisan!',
  'kita belajar bareng yuk buat persiapan ujian',
  'lo tuh ga ada gunanya, semua orang benci sama lo',
  'makasih udah bantuin aku tadi, baik banget',
  'bodoh banget sih, ga ada otak',
  'selamat ulang tahun ya, semoga sukses selalu',
  'mending lo minggat aja dari sini',
  'kerja bagus tadi, presentasinya keren!',
]

const COLORS = {
  bullying: '#ef4444',
  safe: '#10b981',
  high: '#ef4444',
  mid: '#f59e0b',
  low: '#10b981',
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm shadow-lg">
        <p className="text-slate-200 font-medium">{label}</p>
        {payload.map((p, i) => (
          <p key={i} style={{ color: p.color }}>{p.name}: {p.value}</p>
        ))}
      </div>
    )
  }
  return null
}

export default function DashboardPage() {
  const [apiStatus, setApiStatus] = useState(null)
  const [batchResult, setBatchResult] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getHealth()
      .then(setApiStatus)
      .catch(() => setApiStatus({ status: 'error', model_ready: false }))
  }, [])

  const runDemo = async () => {
    setLoading(true)
    try {
      const data = await predictBatch(DEMO_TEXTS)
      setBatchResult(data)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  // Data untuk chart
  const pieData = batchResult
    ? [
        { name: 'Bullying', value: batchResult.n_bullying },
        { name: 'Aman', value: batchResult.n_non_bullying },
      ]
    : null

  const barData = batchResult
    ? batchResult.predictions.map((p, i) => ({
        name: `T${i + 1}`,
        bullying: Math.round(p.confidence_bullying * 100),
        aman: Math.round(p.confidence_non_bullying * 100),
        label: p.label,
      }))
    : null

  const riskDistrib = batchResult
    ? {
        tinggi: batchResult.predictions.filter(p => p.risk_level.includes('Tinggi')).length,
        sedang: batchResult.predictions.filter(p => p.risk_level.includes('Sedang')).length,
        rendah: batchResult.predictions.filter(p => p.risk_level.includes('Rendah')).length,
      }
    : null

  return (
    <div className="max-w-5xl mx-auto fade-in">
      <PageHeader
        title="Dashboard"
        description="Gambaran umum performa model dan demo analisis batch."
        icon={BarChart2}
        iconColor="text-emerald-400"
      />

      {/* Status cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="card flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${apiStatus?.model_ready ? 'bg-emerald-500/20' : 'bg-slate-700'}`}>
            <Shield className={`w-6 h-6 ${apiStatus?.model_ready ? 'text-emerald-400' : 'text-slate-500'}`} />
          </div>
          <div>
            <p className="text-xs text-slate-400">Status Model</p>
            <p className={`font-bold ${apiStatus?.model_ready ? 'text-emerald-400' : 'text-slate-500'}`}>
              {apiStatus === null ? 'Menghubungkan...' : apiStatus.model_ready ? 'Aktif' : 'Offline'}
            </p>
          </div>
        </div>

        <div className="card flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-violet-500/20 flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-violet-400" />
          </div>
          <div>
            <p className="text-xs text-slate-400">Algoritma</p>
            <p className="font-bold text-slate-200">Logistic Regression</p>
          </div>
        </div>

        <div className="card flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center">
            <BarChart2 className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <p className="text-xs text-slate-400">Demo Dataset</p>
            <p className="font-bold text-slate-200">{DEMO_TEXTS.length} teks</p>
          </div>
        </div>
      </div>

      {/* Demo batch analysis */}
      <div className="card mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-white font-bold">Demo Analisis Batch</h3>
            <p className="text-slate-400 text-sm mt-0.5">
              Jalankan {DEMO_TEXTS.length} contoh teks sekaligus untuk melihat performa model.
            </p>
          </div>
          <button
            className="btn-primary flex items-center gap-2"
            onClick={runDemo}
            disabled={loading || !apiStatus?.model_ready}
          >
            {loading ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Memproses...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Jalankan Demo
              </>
            )}
          </button>
        </div>

        {!batchResult && !loading && (
          <div className="text-center py-8 text-slate-500">
            <BarChart2 className="w-10 h-10 mx-auto mb-3 opacity-30" />
            <p className="text-sm">Klik "Jalankan Demo" untuk melihat hasil visualisasi</p>
          </div>
        )}

        {batchResult && (
          <div className="fade-in space-y-6">
            {/* Ringkasan */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-slate-900 rounded-xl p-4 text-center border border-slate-700/50">
                <p className="text-3xl font-bold text-white">{batchResult.total}</p>
                <p className="text-slate-400 text-xs mt-1">Total Teks</p>
              </div>
              <div className="bg-red-500/10 rounded-xl p-4 text-center border border-red-500/25">
                <p className="text-3xl font-bold text-red-400 flex items-center justify-center gap-2">
                  <AlertTriangle className="w-6 h-6" />
                  {batchResult.n_bullying}
                </p>
                <p className="text-slate-400 text-xs mt-1">Terdeteksi Bullying</p>
              </div>
              <div className="bg-emerald-500/10 rounded-xl p-4 text-center border border-emerald-500/25">
                <p className="text-3xl font-bold text-emerald-400 flex items-center justify-center gap-2">
                  <CheckCircle className="w-6 h-6" />
                  {batchResult.n_non_bullying}
                </p>
                <p className="text-slate-400 text-xs mt-1">Aman</p>
              </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Pie chart */}
              <div>
                <p className="text-sm font-medium text-slate-300 mb-3">Distribusi Hasil</p>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={55}
                      outerRadius={90}
                      paddingAngle={3}
                      dataKey="value"
                    >
                      <Cell fill={COLORS.bullying} />
                      <Cell fill={COLORS.safe} />
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                    <Legend
                      formatter={(value) => <span className="text-slate-300 text-sm">{value}</span>}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Bar chart distribusi risiko */}
              <div>
                <p className="text-sm font-medium text-slate-300 mb-3">Distribusi Level Risiko</p>
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart
                    data={[
                      { name: '🔴 Tinggi', value: riskDistrib.tinggi, fill: COLORS.high },
                      { name: '🟡 Sedang', value: riskDistrib.sedang, fill: COLORS.mid },
                      { name: '🟢 Rendah', value: riskDistrib.rendah, fill: COLORS.low },
                    ]}
                    margin={{ top: 5, right: 10, bottom: 5, left: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                    <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} allowDecimals={false} />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="value" name="Jumlah" radius={[4, 4, 0, 0]}>
                      {[COLORS.high, COLORS.mid, COLORS.low].map((color, i) => (
                        <Cell key={i} fill={color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Confidence bar chart per teks */}
            <div>
              <p className="text-sm font-medium text-slate-300 mb-3">Probabilitas per Teks</p>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={barData} margin={{ top: 5, right: 10, bottom: 5, left: 0 }} stackOffset="expand">
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                  <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} tickFormatter={(v) => `${v}%`} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend formatter={(value) => <span className="text-slate-300 text-sm">{value}</span>} />
                  <Bar dataKey="aman" name="Aman %" stackId="a" fill={COLORS.safe} />
                  <Bar dataKey="bullying" name="Bullying %" stackId="a" fill={COLORS.bullying} radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Detail tabel */}
            <div>
              <p className="text-sm font-medium text-slate-300 mb-3">Detail Hasil</p>
              <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                {batchResult.predictions.map((p, i) => (
                  <div
                    key={i}
                    className={`rounded-lg p-3 flex items-start gap-3 border ${
                      p.label === 1
                        ? 'bg-red-500/8 border-red-500/20'
                        : 'bg-slate-900 border-slate-700/40'
                    }`}
                  >
                    <span className="text-xs text-slate-600 w-5 flex-shrink-0 pt-0.5">{i + 1}.</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-slate-200 truncate">{p.text_original}</p>
                      <div className="mt-1.5">
                        <ConfidenceBar
                          confidenceBullying={p.confidence_bullying}
                          confidenceNonBullying={p.confidence_non_bullying}
                          showLabels={false}
                        />
                      </div>
                    </div>
                    <RiskBadge riskLevel={p.risk_level} label={p.label} size="sm" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Info model */}
      <div className="card border-violet-500/20">
        <h3 className="text-white font-bold mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-violet-400" />
          Tentang Model
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
          {[
            { label: 'Algoritma', value: 'Logistic Regression' },
            { label: 'Feature Extraction', value: 'TF-IDF + Lexical Features' },
            { label: 'Preprocessing', value: 'Tokenisasi, Normalisasi, Stop-word removal' },
            { label: 'Output', value: 'Label Biner + Probabilitas' },
            { label: 'Bahasa', value: 'Bahasa Indonesia (informal/slang)' },
            { label: 'Use Case', value: 'Moderasi chat, Deteksi perundungan' },
          ].map(({ label, value }) => (
            <div key={label} className="bg-slate-900 rounded-lg px-4 py-3">
              <p className="text-slate-500 text-xs">{label}</p>
              <p className="text-slate-200 font-medium mt-0.5">{value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
