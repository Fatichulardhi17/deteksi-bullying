# BullyGuard — Sistem Deteksi Bullying Bahasa Indonesia

Frontend React JS untuk merepresentasikan model deteksi bullying berbasis Machine Learning.

## Struktur Proyek

```
web/
├── api.py                          # Backend Flask API
├── requirements.txt                # Dependencies Python
├── bullying_detection/             # Modul ML
│   ├── inference/detector.py       # BullyingDetector class
│   ├── features/                   # Feature extraction
│   ├── preprocessing/              # Text preprocessing
│   └── saved_model/                # Model tersimpan (.pkl)
└── frontend/                       # React + Vite frontend
    ├── src/
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   ├── PageHeader.jsx
    │   │   ├── StatusIndicator.jsx
    │   │   ├── RiskBadge.jsx
    │   │   ├── ConfidenceBar.jsx
    │   │   └── KeywordChips.jsx
    │   ├── pages/
    │   │   ├── DashboardPage.jsx   # Dashboard + batch demo
    │   │   ├── PredictPage.jsx     # Prediksi individual
    │   │   └── ConversationPage.jsx # Analisis percakapan
    │   ├── services/api.js         # Axios/fetch ke backend
    │   └── App.jsx
    └── vite.config.js
```

## Menjalankan Aplikasi

### 1. Backend (Flask API)

```bash
# Aktifkan virtual environment
.venv\Scripts\activate          # Windows
# atau
source .venv/bin/activate       # Linux/Mac

# Install dependencies jika belum
pip install flask flask-cors

# Jalankan server
python api.py
```

Server berjalan di: `http://localhost:5000`

### 2. Frontend (React)

Buka terminal baru:

```bash
cd frontend
npm install
npm run dev
```

Frontend berjalan di: `http://localhost:5173`

## Fitur

| Halaman | Deskripsi |
|---------|-----------|
| **Dashboard** | Statistik umum, demo batch 10 teks, visualisasi pie chart & bar chart |
| **Prediksi Teks** | Input satu teks, tampilkan label, probabilitas, keyword, fitur leksikal |
| **Analisis Percakapan** | Input multi-pesan, analisis per pengirim, timeline pesan |

## Endpoint API

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/health` | Status API dan model |
| POST | `/predict` | Prediksi satu teks |
| POST | `/predict/batch` | Prediksi banyak teks (max 100) |
| POST | `/analyze` | Analisis percakapan |

### Contoh Request

**POST /predict**
```json
{ "text": "dasar goblok, malu-maluin aja" }
```

**POST /analyze**
```json
{
  "messages": [
    { "sender": "Budi", "text": "dasar bego lo!" },
    { "sender": "Siti", "text": "jangan kasar dong" }
  ]
}
```

## Teknologi

- **Frontend**: React 19, Vite, Tailwind CSS v4, Recharts, Lucide React
- **Backend**: Flask, Flask-CORS
- **ML**: Scikit-learn (Logistic Regression), TF-IDF, Custom Lexical Features
