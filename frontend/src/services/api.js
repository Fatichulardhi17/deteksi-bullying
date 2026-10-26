/**
 * API service layer — semua komunikasi ke Flask backend.
 * Base URL: /api (di-proxy ke http://localhost:5000 oleh Vite)
 */

const BASE_URL = '/api'

/**
 * Fetch wrapper dengan error handling terpusat.
 */
async function apiFetch(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || `HTTP ${response.status}`)
  }

  return data
}

/**
 * Cek status API & model.
 */
export async function getHealth() {
  return apiFetch('/health')
}

/**
 * Prediksi satu teks.
 * @param {string} text
 * @returns {Promise<PredictionResult>}
 */
export async function predictText(text) {
  return apiFetch('/predict', {
    method: 'POST',
    body: JSON.stringify({ text }),
  })
}

/**
 * Prediksi banyak teks sekaligus.
 * @param {string[]} texts
 * @returns {Promise<BatchResult>}
 */
export async function predictBatch(texts) {
  return apiFetch('/predict/batch', {
    method: 'POST',
    body: JSON.stringify({ texts }),
  })
}

/**
 * Analisis percakapan.
 * @param {{ sender: string, text: string }[]} messages
 * @returns {Promise<ConversationAnalysis>}
 */
export async function analyzeConversation(messages) {
  return apiFetch('/analyze', {
    method: 'POST',
    body: JSON.stringify({ messages }),
  })
}
