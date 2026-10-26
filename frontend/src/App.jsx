import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import StatusIndicator from './components/StatusIndicator'
import DashboardPage from './pages/DashboardPage'
import PredictPage from './pages/PredictPage'
import ConversationPage from './pages/ConversationPage'

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-950">
        {/* Sidebar */}
        <Navbar />

        {/* Main content */}
        <div className="flex-1 ml-64 flex flex-col min-h-screen">
          {/* Top bar */}
          <header className="sticky top-0 z-10 bg-slate-950/80 backdrop-blur-sm border-b border-slate-800 px-8 py-3 flex items-center justify-between">
            <p className="text-sm text-slate-500">
              Sistem Deteksi Bullying &mdash; Bahasa Indonesia
            </p>
            <StatusIndicator />
          </header>

          {/* Page content */}
          <main className="flex-1 px-8 py-8">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/predict" element={<PredictPage />} />
              <Route path="/conversation" element={<ConversationPage />} />
            </Routes>
          </main>

          {/* Footer */}
          <footer className="px-8 py-4 border-t border-slate-800 text-xs text-slate-600 text-center">
            BullyGuard &copy; 2026 &mdash; Model berbasis Logistic Regression untuk deteksi bullying bahasa Indonesia
          </footer>
        </div>
      </div>
    </BrowserRouter>
  )
}
