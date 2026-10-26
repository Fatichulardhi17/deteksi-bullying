# RANGKUMAN KODE — BullyGuard: Sistem Deteksi Bullying Bahasa Indonesia

> Dibuat otomatis pada: 2026-08-04  
> Tujuan: Dokumentasi lengkap setiap file kode dalam proyek ini.

---

## Daftar Isi

1. [Gambaran Umum Proyek](#1-gambaran-umum-proyek)
2. [Struktur Folder](#2-struktur-folder)
3. [Backend](#3-backend)
   - [requirements.txt](#31-requirementstxt)
   - [api.py](#32-apipy)
4. [Modul Machine Learning](#4-modul-machine-learning)
   - [bullying_detection/__init__.py](#41-bullying_detection__init__py)
   - [data/dataset.py](#42-datadatasetpy)
   - [preprocessing/text_preprocessor.py](#43-preprocessingtext_preprocessorpy)
   - [features/feature_extractor.py](#44-featuresfeature_extractorpy)
   - [models/trainer.py](#45-modelstrainerpy)
   - [inference/detector.py](#46-inferencedetectorpy)
5. [Frontend](#5-frontend)
   - [vite.config.js](#51-viteconfigjs)
   - [src/main.jsx](#52-srcmainjsx)
   - [src/App.jsx](#53-srcappjsx)
   - [src/services/api.js](#54-srcservicesapijs)
   - [Komponen UI](#55-komponen-ui)
   - [Halaman (Pages)](#56-halaman-pages)
6. [Alur Kerja Sistem](#7-alur-kerja-sistem)

---

## 1. Gambaran Umum Proyek

**BullyGuard** adalah aplikasi web full-stack untuk mendeteksi konten bullying dalam teks berbahasa Indonesia (termasuk bahasa gaul/informal). Sistem ini menggunakan pendekatan Machine Learning klasik dengan dua lapisan fitur:

- **TF-IDF** — representasi statistik kemunculan kata
- **Lexical Features** — deteksi berbasis kamus kata bullying (kata kasar, ancaman, pengucilan, dll.)

Arsitektur sistem:
- **Backend**: Python + Flask → memuat model ML dan menyajikan REST API
- **Frontend**: React + Vite + Tailwind CSS → antarmuka pengguna
- **Model ML**: Logistic Regression (dipilih sebagai model terbaik dari 4 kandidat)

---

## 2. Struktur Folder

```
deteksi-bullying/
├── api.py                              # Server Flask (entry point backend)
├── requirements.txt                    # Dependensi Python
├── bullying_detection_analysis.ipynb  # Notebook eksplorasi/eksperimen
│
├── bullying_detection/                 # Package modul ML
│   ├── __init__.py
│   ├── data/
│   │   └── dataset.py                  # 90 sampel teks berlabel
│   ├── preprocessing/
│   │   └── text_preprocessor.py        # Pipeline NLP (cleaning, normalisasi, stopword)
│   ├── features/
│   │   └── feature_extractor.py        # TF-IDF + Lexical Feature Extractor
│   ├── models/
│   │   └── trainer.py                  # Training & evaluasi 4 model ML
│   ├── inference/
│   │   └── detector.py                 # BullyingDetector (interface utama)
│   └── saved_model/
│       ├── model.pkl                   # Model Logistic Regression tersimpan
│       ├── extractor.pkl               # Feature extractor tersimpan
│       └── scaler.pkl                  # Scaler tersimpan
│
└── frontend/                           # Aplikasi React
    ├── vite.config.js                  # Konfigurasi Vite + proxy API
    ├── package.json
    └── src/
        ├── main.jsx                    # Entry point React
        ├── App.jsx                     # Root component + routing
        ├── index.css                   # Global styles (Tailwind)
        ├── services/
        │   └── api.js                  # Layer komunikasi ke backend
        ├── components/
        │   ├── Navbar.jsx              # Sidebar navigasi
        │   ├── PageHeader.jsx          # Header konsisten tiap halaman
        │   ├── StatusIndicator.jsx     # Indikator koneksi backend
        │   ├── RiskBadge.jsx           # Badge level risiko berwarna
        │   ├── ConfidenceBar.jsx       # Progress bar probabilitas
        │   └── KeywordChips.jsx        # Chip/tag kata kunci bullying
        └── pages/
            ├── DashboardPage.jsx       # Statistik umum + demo batch
            ├── PredictPage.jsx         # Prediksi teks individual
            └── ConversationPage.jsx    # Analisis percakapan multi-pesan
```

---


## 3. Backend

### 3.1 `requirements.txt`

File daftar dependensi Python yang dibutuhkan untuk menjalankan proyek.

| Package | Versi Minimum | Kegunaan |
|---|---|---|
| `scikit-learn` | 1.5.0 | Model ML (Logistic Regression, SVM, dll.), TF-IDF, evaluasi |
| `numpy` | 2.0.0 | Operasi array/matriks numerik |
| `scipy` | 1.13.0 | Sparse matrix (hasil TF-IDF) |
| `pandas` | 2.2.0 | Manipulasi dataset (DataFrame) |
| `matplotlib` | 3.8.0 | Visualisasi grafik (untuk notebook) |
| `seaborn` | 0.13.0 | Visualisasi statistik (untuk notebook) |
| `jupyter` | 1.0.0 | Notebook eksplorasi |
| `ipykernel` | 6.29.0 | Kernel Jupyter |

> Catatan: `transformers` dan `torch` dikomentari — tersedia sebagai opsi upgrade ke model berbasis Transformer di masa depan.

---

### 3.2 `api.py`

**Peran**: Entry point backend. Server Flask yang menerima request HTTP dari frontend dan mengembalikan hasil prediksi.

**Cara kerja saat startup**:
1. Flask app dibuat, CORS diaktifkan (agar frontend React bisa mengakses)
2. `BullyingDetector` diinisialisasi
3. Sistem mencoba **memuat model tersimpan** dari `bullying_detection/saved_model/`
4. Jika gagal → otomatis **melatih model baru** dengan Logistic Regression dan menyimpannya

**Helper function**:
- `prediction_to_dict(result)` — mengkonversi objek `PredictionResult` menjadi dict Python agar bisa di-serialize ke JSON

**Endpoint yang tersedia**:

| Method | Path | Fungsi |
|---|---|---|
| `GET` | `/` | Info API dan daftar endpoint |
| `GET` | `/health` | Status API: apakah model sudah siap |
| `POST` | `/predict` | Prediksi **satu** teks |
| `POST` | `/predict/batch` | Prediksi **banyak** teks (maks. 100) |
| `POST` | `/analyze` | Analisis **percakapan** (list pesan berurutan, maks. 200) |

**Detail tiap endpoint**:

- **`/predict`** — Menerima `{ "text": "..." }`, mengembalikan label, probabilitas, keyword, dan fitur leksikal.
- **`/predict/batch`** — Menerima `{ "texts": [...] }`, mengembalikan agregat (total, n_bullying, rasio) + detail tiap teks.
- **`/analyze`** — Menerima `{ "messages": [{"sender": "...", "text": "..."}, ...] }`. Mengembalikan statistik per pengirim, pesan yang ditandai, dan detail prediksi tiap pesan.

**Validasi input**:
- Teks kosong ditolak dengan HTTP 400
- Batch > 100 teks ditolak
- Percakapan > 200 pesan ditolak
- Jika field `sender` tidak ada pada `/analyze`, otomatis diisi `User1`, `User2`, dst.

```python
# Contoh request /predict
POST /predict
{ "text": "dasar goblok, malu-maluin aja" }

# Contoh response
{
  "label": 1,
  "label_str": "⚠️ Bullying",
  "confidence": 0.92,
  "confidence_bullying": 0.92,
  "confidence_non_bullying": 0.08,
  "risk_level": "🔴 Tinggi",
  "detected_keywords": ["goblok"],
  "lexical_features": { "jumlah_kata_kasar": 1.0, ... },
  "warning_message": "Konten ini berpotensi menyebabkan trauma psikologis."
}
```

---


## 4. Modul Machine Learning

### 4.1 `bullying_detection/__init__.py`

File kosong yang menandai folder `bullying_detection/` sebagai Python package, sehingga modul di dalamnya bisa diimport dengan `from bullying_detection.xxx import yyy`.

---

### 4.2 `data/dataset.py`

**Peran**: Menyediakan dataset pelatihan model dalam bentuk hardcoded (tidak perlu file CSV eksternal).

**Isi dataset**:
- Total **90 sampel** teks berbahasa Indonesia
- **45 sampel bullying** (`label = 1`) dan **45 sampel non-bullying** (`label = 0`)
- Dataset seimbang (*balanced*) — penting agar model tidak bias ke satu kelas

**Kategori teks bullying yang dicakup**:
| Kategori | Contoh |
|---|---|
| Hinaan fisik | "dasar jelek banget muka lo, kayak hantu" |
| Hinaan kecerdasan | "bego banget sih lo, ga bisa apa-apa" |
| Ancaman | "awas lo ya, besok ketemu aku hajar" |
| Pengucilan sosial | "ga ada yang mau temenan sama lo, sendirian aja sana" |
| Cyberbullying / gosip | "gue screenshot chat lo terus gue sebar ya" |
| Kata kasar / makian | "bangsat lo, nyebelin banget sih" |
| Meremehkan | "lo ga akan pernah bisa sukses, percuma aja hidup" |
| Ejekan identitas | "miskin kayak lo masih sok-sokan" |
| Ejekan prestasi | "lo tuh beban kelompok, mending ga usah ikut" |

**Kategori teks non-bullying yang dicakup**:
Percakapan sehari-hari, diskusi pelajaran, olahraga & kegiatan, pujian & dukungan, empati, humor ringan, koordinasi, dan berbagi informasi.

**Fungsi yang tersedia**:
- `get_dataframe()` — mengembalikan dataset sebagai `pandas.DataFrame` dengan kolom `text` dan `label`
- `get_class_distribution(df)` — mencetak distribusi kelas ke konsol

---

### 4.3 `preprocessing/text_preprocessor.py`

**Peran**: Membersihkan dan menormalisasi teks mentah sebelum dimasukkan ke model.

**Konstanta penting**:
- `STOPWORDS_ID` — set ~100+ kata umum bahasa Indonesia yang tidak informatif untuk klasifikasi (kata ganti, konjungsi, partikel, dll.)
- `SLANG_DICT` — kamus ~100+ kata slang/gaul ke bentuk bakunya. Contoh: `"gue" → "saya"`, `"goblok" → "bodoh"`, `"makasih" → "terima kasih"`

**Pipeline preprocessing** (urutan eksekusi di fungsi `preprocess()`):

```
1. lowercase()               → semua huruf menjadi kecil
2. remove_url()              → hapus URL (http://, www., dll.)
3. remove_mentions_hashtags()→ hapus @mention dan #hashtag
4. remove_emoji()            → hapus emoji unicode
5. normalize_repeated_chars()→ "goblooook" → "goblok" (maks. 2 karakter berulang)
6. normalize_slang()         → ganti kata slang dengan padanan baku
7. remove_punctuation()      → hapus tanda baca
8. remove_numbers()          → hapus angka
9. remove_extra_whitespace() → normalisasi spasi
10. remove_stopwords()       → hapus kata tidak informatif (opsional, default: aktif)
```

**Fungsi utama**:
- `preprocess(text, remove_stop=True)` → memproses satu teks, mengembalikan string bersih
- `preprocess_batch(texts, remove_stop=True)` → memproses list teks sekaligus

**Contoh transformasi**:
```
Input : "dasar GOBLOK banget sih lo!! ga bisa apa-apa 😤"
Output: "dasar bodoh"
```
(GOBLOK → bodoh via slang dict, "banget/sih/lo/ga/bisa/apa-apa" dihapus stopwords, tanda baca & emoji dihapus)

---


### 4.4 `features/feature_extractor.py`

**Peran**: Mengubah teks yang sudah diproses menjadi vektor angka yang bisa dipahami model ML. Menggabungkan dua jenis fitur: TF-IDF dan fitur leksikal.

#### Kamus Kata Bullying (Lexicon)

File ini mendefinisikan 5 set kata bullying:

| Set | Contoh isi |
|---|---|
| `KATA_KASAR` | anjing, goblok, bangsat, brengsek, idiot, sampah |
| `KATA_ANCAMAN` | hajar, bunuh, ancam, balas, gebuk, pukul |
| `KATA_PENGUCILAN` | pergi, enyah, sendirian, dikucilkan, tidak berteman |
| `KATA_MERENDAHKAN` | jelek, miskin, norak, loser, gagal, pecundang |
| `KATA_GOSIP` | screenshot, sebar, viral, expose, fitnah |

Semua set digabung menjadi `ALL_BULLYING_WORDS` untuk pengecekan cepat.

#### Class `LexicalFeatureExtractor`

Mengekstrak **11 fitur numerik** dari satu teks:

| No | Nama Fitur | Cara Hitung |
|---|---|---|
| 1 | `jumlah_kata_kasar` | hitung token yang ada di `KATA_KASAR` |
| 2 | `jumlah_kata_ancaman` | hitung token yang ada di `KATA_ANCAMAN` |
| 3 | `jumlah_kata_pengucilan` | hitung token yang ada di `KATA_PENGUCILAN` |
| 4 | `jumlah_kata_merendahkan` | hitung token yang ada di `KATA_MERENDAHKAN` |
| 5 | `jumlah_kata_gosip` | hitung token yang ada di `KATA_GOSIP` |
| 6 | `rasio_kata_bullying` | (jumlah kata bullying) / (total kata) |
| 7 | `panjang_teks` | jumlah kata dalam teks |
| 8 | `jumlah_tanda_seru` | hitung karakter `!` |
| 9 | `jumlah_huruf_kapital` | hitung huruf kapital (indikasi "teriak") |
| 10 | `mengandung_ancaman_fisik` | biner: 1 jika ada kata ancaman fisik |
| 11 | `mengandung_sebar_informasi` | biner: 1 jika ada kata penyebaran info |

Metode: `extract(text)` → `np.ndarray` shape `(11,)` | `extract_batch(texts)` → shape `(n, 11)`

#### Class `BullyingFeatureExtractor`

Menggabungkan TF-IDF dan fitur leksikal menjadi satu matriks fitur:

```
[TF-IDF sparse matrix (n × 5000)] + [Lexical dense matrix (n × 11)]
= Combined sparse matrix (n × 5011)
```

Parameter TF-IDF:
- `max_features=5000` — ambil 5000 kata paling informatif
- `ngram_range=(1,2)` — unigram dan bigram
- `sublinear_tf=True` — gunakan `log(1+tf)` untuk mengurangi bias kata frekuensi tinggi

Metode:
- `fit(texts)` — fit TF-IDF pada data training
- `transform(texts)` → sparse matrix fitur gabungan
- `fit_transform(texts)` — fit + transform sekaligus
- `get_feature_names()` → daftar nama semua fitur

---

### 4.5 `models/trainer.py`

**Peran**: Melatih, mengevaluasi, dan membandingkan beberapa model ML untuk memilih yang terbaik.

#### Konfigurasi 4 Model (`MODEL_CONFIG`)

| Nama | Algoritma | Konfigurasi Penting |
|---|---|---|
| `naive_bayes` | Complement Naive Bayes | `alpha=0.5` |
| `logistic_regression` | Logistic Regression | `C=1.0`, `class_weight="balanced"`, `max_iter=1000` |
| `svm` | LinearSVC + CalibratedClassifierCV | `C=1.0`, `class_weight="balanced"`, dikalibrasi agar bisa output probabilitas |
| `random_forest` | Random Forest | `n_estimators=100`, `max_depth=10`, `class_weight="balanced"` |

Semua model menggunakan `class_weight="balanced"` untuk menangani ketidakseimbangan kelas.

#### Class `BullyingModelTrainer`

Alur penggunaan:
```
1. split_data(X, y)     → stratified train/test split (default 80/20)
2. scale_features()     → normalisasi dengan MaxAbsScaler (aman untuk sparse matrix)
3. train_all()          → latih semua 4 model
4. evaluate_all()       → hitung metrik untuk semua model
5. select_best_model()  → pilih model terbaik berdasarkan F1-Score
6. save_model()         → simpan model ke .pkl
7. save_scaler()        → simpan scaler ke .pkl
```

**Metrik evaluasi yang dihitung**:
- Accuracy, Precision, Recall, F1-Score, AUC-ROC
- Confusion Matrix (TN, FP, FN, TP)
- Classification Report lengkap per kelas

**Method penting**:
- `cross_validate(model_name, X, y, cv=5)` → cross-validation dengan StratifiedKFold
- `get_comparison_table()` → tabel perbandingan semua model sebagai DataFrame
- `print_results()` → cetak ringkasan evaluasi ke konsol

---


### 4.6 `inference/detector.py`

**Peran**: Interface utama sistem — satu-satunya class yang perlu dipakai oleh `api.py`. Menyatukan semua pipeline dari preprocessing → ekstraksi fitur → prediksi.

#### Data Classes

**`PredictionResult`** — hasil prediksi satu teks:
| Field | Tipe | Keterangan |
|---|---|---|
| `text_original` | str | Teks asli sebelum diproses |
| `text_processed` | str | Teks setelah preprocessing |
| `label` | int | 0 = tidak bullying, 1 = bullying |
| `label_str` | str | "✅ Tidak Bullying" atau "⚠️ Bullying" |
| `confidence` | float | Probabilitas kelas yang diprediksi (0–1) |
| `confidence_bullying` | float | Probabilitas kelas bullying |
| `confidence_non_bullying` | float | Probabilitas kelas tidak bullying |
| `risk_level` | str | "🔴 Tinggi" / "🟡 Sedang" / "🟢 Rendah" |
| `detected_keywords` | list | Kata-kata bullying yang ditemukan |
| `lexical_features` | dict | Fitur leksikal yang bernilai > 0 |
| `warning_message` | str | Pesan peringatan (jika bullying) |

**Level risiko** ditentukan dari `confidence_bullying`:
- ≥ 0.7 → 🔴 Tinggi
- 0.4–0.7 → 🟡 Sedang
- < 0.4 → 🟢 Rendah

**`BatchPredictionResult`** — hasil prediksi banyak teks: berisi list `PredictionResult` + statistik agregat (total, n_bullying, n_non_bullying, bullying_ratio).

#### Class `BullyingDetector`

**Method setup**:
- `train(df, model_name, save_dir)` — melatih model dari nol. Jika `df=None`, memakai dataset bawaan. Jika `save_dir` diisi, model disimpan otomatis.
- `save(save_dir)` — menyimpan `model.pkl`, `extractor.pkl`, dan `scaler.pkl`
- `load(save_dir)` — memuat ketiga file `.pkl` dari disk

**Method prediksi**:

`predict(text)` — pipeline lengkap untuk satu teks:
```
teks mentah
  → preprocess()             [text_preprocessor.py]
  → extractor.transform()    [BullyingFeatureExtractor]
  → scaler.transform()       [MaxAbsScaler]
  → model.predict()          [Logistic Regression]
  → model.predict_proba()    [probabilitas]
  → _detect_keywords()       [cari kata di ALL_BULLYING_WORDS]
  → _build_lexical_info()    [hitung 11 fitur leksikal]
  → PredictionResult
```

`predict_batch(texts)` — memanggil `predict()` untuk setiap teks, mengembalikan `BatchPredictionResult`.

`analyze_conversation(messages)` — analisis list pesan:
- Prediksi setiap pesan satu per satu
- Akumulasi statistik per `sender`: total pesan, pesan bullying, rata-rata risk score
- Kumpulkan semua pesan yang ditandai sebagai bullying (`flagged_messages`)
- Mengembalikan dict lengkap dengan `sender_stats`, `flagged_messages`, dan `status`

---


## 5. Frontend

### 5.1 `vite.config.js`

**Peran**: Konfigurasi build tool Vite untuk project React.

**Plugin yang digunakan**:
- `@vitejs/plugin-react` — dukungan JSX dan React Fast Refresh
- `@tailwindcss/vite` — integrasi Tailwind CSS v4 langsung lewat Vite

**Konfigurasi proxy**:
```js
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ''),
  }
}
```
Setiap request ke `/api/xxx` dari frontend akan diteruskan ke `http://localhost:5000/xxx` (Flask). Ini menghindari masalah CORS saat development dan menyembunyikan alamat backend dari browser.

---

### 5.2 `src/main.jsx`

**Peran**: Entry point aplikasi React. File pertama yang dieksekusi.

```jsx
createRoot(document.getElementById('root')).render(
  <StrictMode><App /></StrictMode>
)
```
Merender komponen `<App />` ke dalam elemen `<div id="root">` di `index.html`. `StrictMode` mengaktifkan peringatan ekstra saat development.

---

### 5.3 `src/App.jsx`

**Peran**: Root component yang mendefinisikan layout global dan routing halaman.

**Layout global**:
```
┌─────────────────────────────────────────────┐
│  Sidebar (Navbar, w-64, fixed)              │
│  ┌───────────────────────────────────────┐  │
│  │  Header (sticky, StatusIndicator)    │  │
│  │  ───────────────────────────────     │  │
│  │  <main>                              │  │
│  │    <Routes>                          │  │
│  │      /           → DashboardPage     │  │
│  │      /predict    → PredictPage       │  │
│  │      /conversation→ConversationPage  │  │
│  │    </Routes>                         │  │
│  │  </main>                             │  │
│  │  Footer                              │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

Menggunakan `react-router-dom` v6 dengan `BrowserRouter` + `Routes` + `Route`.

---

### 5.4 `src/services/api.js`

**Peran**: Layer abstraksi untuk semua komunikasi HTTP ke backend Flask.

**Fetch wrapper `apiFetch()`**: menambahkan header `Content-Type: application/json` secara otomatis dan melempar `Error` jika response tidak OK.

**Fungsi yang diekspor**:

| Fungsi | Method | Endpoint | Keterangan |
|---|---|---|---|
| `getHealth()` | GET | `/api/health` | Cek status model |
| `predictText(text)` | POST | `/api/predict` | Prediksi satu teks |
| `predictBatch(texts)` | POST | `/api/predict/batch` | Prediksi banyak teks |
| `analyzeConversation(messages)` | POST | `/api/analyze` | Analisis percakapan |

---

### 5.5 Komponen UI

#### `Navbar.jsx`
Sidebar navigasi kiri yang fixed. Berisi:
- Logo BullyGuard (ikon Shield ungu dengan dot hijau)
- 3 link navigasi: Dashboard, Prediksi Teks, Analisis Percakapan
- Link aktif di-highlight dengan warna ungu (`bg-violet-600/20`)
- Footer kecil bertuliskan "Hanya untuk edukasi" + nama model

#### `PageHeader.jsx`
Header konsisten yang tampil di atas setiap halaman. Menerima props:
- `title` — judul halaman
- `description` — deskripsi singkat
- `icon` — Lucide icon component
- `iconColor` — warna ikon (default: `text-violet-400`)

#### `StatusIndicator.jsx`
Indikator di pojok kanan atas header yang menampilkan status koneksi ke backend. Polling setiap **30 detik** ke endpoint `/health`.
- ⬛ Menghubungkan... (saat loading awal)
- 🔴 Backend offline (jika gagal / model belum siap)
- 🟢 Model aktif (jika backend online dan model siap)

#### `RiskBadge.jsx`
Badge berwarna berbentuk pill yang menampilkan level risiko. Props: `riskLevel`, `label`, `size` (sm/md/lg).
- Label 0 → badge hijau "Aman"
- Label 1, risiko Tinggi → badge merah "Risiko Tinggi"
- Label 1, risiko Sedang → badge kuning "Risiko Sedang"

#### `ConfidenceBar.jsx`
Progress bar horizontal dua warna yang menampilkan distribusi probabilitas:
- Sisi kiri (hijau) → probabilitas aman
- Sisi kanan (merah) → probabilitas bullying
- Persentase ditampilkan di dalam bar jika lebar ≥ 15%
- Animasi transisi 500ms dengan `ease-out`

#### `KeywordChips.jsx`
Menampilkan kata-kata bullying yang terdeteksi sebagai chip/tag berwarna merah. Jika tidak ada keyword → menampilkan pesan "Tidak ada kata kunci bullying terdeteksi" dengan ikon ✅.

---


### 5.6 Halaman (Pages)

#### `DashboardPage.jsx`

**Peran**: Halaman utama yang menampilkan gambaran umum sistem dan demo analisis batch.

**State**:
- `apiStatus` — hasil `/health` untuk menampilkan kartu status model
- `batchResult` — hasil dari `predictBatch()` setelah demo dijalankan

**Komponen tampilan**:
1. **3 kartu status** — Status Model, Algoritma (Logistic Regression), jumlah teks demo
2. **Tombol "Jalankan Demo"** — mengirim 10 teks hardcoded ke `/predict/batch`
3. **Setelah demo berjalan**, tampil:
   - Ringkasan: total teks / terdeteksi bullying / aman
   - **Pie chart** — distribusi bullying vs aman (Recharts)
   - **Bar chart** — distribusi level risiko (Tinggi/Sedang/Rendah)
   - **Stacked bar chart** — probabilitas per teks (T1–T10)
   - **Tabel detail** — setiap teks dengan mini ConfidenceBar dan RiskBadge
4. **Kartu "Tentang Model"** — informasi teknis model (algoritma, feature extraction, dll.)

**10 teks demo yang digunakan**:
- 5 teks bullying (hinaan, ancaman, pengucilan)
- 5 teks non-bullying (semangat, terima kasih, belajar bareng, dll.)

---

#### `PredictPage.jsx`

**Peran**: Halaman untuk prediksi satu teks secara interaktif.

**State**: `text`, `result`, `loading`, `error`, `showLexical`

**Fitur input**:
- Textarea untuk input teks bebas
- Shortcut **Ctrl+Enter** untuk prediksi cepat
- 6 tombol contoh teks (dipotong 30 karakter jika terlalu panjang)
- Tombol Reset untuk membersihkan semua state

**Tampilan hasil** (muncul setelah prediksi):
1. Teks asli yang dianalisis + `RiskBadge`
2. Kotak status besar (merah untuk bullying, hijau untuk aman) + pesan peringatan jika ada
3. `ConfidenceBar` — distribusi probabilitas
4. `KeywordChips` — kata kunci yang terdeteksi
5. **Accordion fitur leksikal** — dapat dibuka/tutup, tampilkan fitur yang nilainya > 0
6. Teks setelah preprocessing (dalam font monospace)

---

#### `ConversationPage.jsx`

**Peran**: Halaman untuk menganalisis percakapan multi-pesan.

**State**: `messages` (array `{sender, text}`), `result`, `loading`, `error`

**Fitur input**:
- Daftar input dinamis: setiap baris punya field **Pengirim** + **Teks pesan**
- Tombol **+** untuk menambah baris pesan
- Tombol **🗑️** untuk menghapus baris (tidak bisa dihapus jika hanya 1 baris)
- Tekan **Enter** di baris terakhir untuk otomatis tambah baris baru
- Tombol **"Muat Contoh"** — mengisi form dengan 6 pesan percakapan contoh (Budi vs Siti)
- Hanya pesan dengan teks tidak kosong yang dikirim ke API

**Tampilan hasil**:
1. **3 kartu ringkasan** — Total Pesan / Pesan Bullying / Rasio Bullying (%)
2. **Kotak status keseluruhan** — "Percakapan Berisiko" atau "Percakapan Aman"
3. **Statistik per Pengirim** — card untuk tiap sender berisi:
   - Inisial nama (avatar bulat)
   - Rasio `pesan_bullying / total_pesan`
   - Badge "⚠️ Terindikasi" jika ada bullying
   - Rata-rata risk score + mini progress bar
4. **Detail Pesan (Timeline)** — setiap pesan dengan:
   - Nomor urut, nama pengirim, `RiskBadge`
   - Teks pesan
   - `KeywordChips` (jika ada keyword)
   - `ConfidenceBar` mini

---

## 6. Alur Kerja Sistem

### Alur Prediksi Satu Teks (End-to-End)

```
Pengguna ketik teks di PredictPage
       ↓
predictText(text)  [services/api.js]
       ↓
POST /api/predict  [via Vite proxy → Flask :5000/predict]
       ↓
api.py: detector.predict(text)
       ↓
┌─────────────────────────────────────────────┐
│  1. preprocess(text)                        │
│     lowercase → remove URL → remove emoji  │
│     → normalize slang → remove stopwords   │
│                                             │
│  2. extractor.transform([text_clean])       │
│     TF-IDF (5000 fitur) + Lexical (11 fitur)│
│     = sparse matrix (1 × 5011)             │
│                                             │
│  3. scaler.transform(X)                     │
│     MaxAbsScaler normalization             │
│                                             │
│  4. model.predict(X)  → label 0/1          │
│     model.predict_proba(X) → [p0, p1]      │
│                                             │
│  5. _detect_keywords() → kata bullying      │
│  6. _build_lexical_info() → fitur aktif     │
│  7. _get_risk_level() → Rendah/Sedang/Tinggi│
└─────────────────────────────────────────────┘
       ↓
JSON response → PredictPage menampilkan hasil
```

### Relasi Antar Modul Backend

```
api.py
  └── BullyingDetector (detector.py)
        ├── BullyingFeatureExtractor (feature_extractor.py)
        │     ├── TfidfVectorizer (scikit-learn)
        │     └── LexicalFeatureExtractor
        ├── TextPreprocessor (text_preprocessor.py)
        ├── BullyingModelTrainer (trainer.py)  ← hanya saat training
        └── Dataset (dataset.py)              ← hanya saat training
```

### Relasi Antar Komponen Frontend

```
App.jsx (BrowserRouter)
  ├── Navbar.jsx (sidebar fixed)
  ├── StatusIndicator.jsx (polling /health)
  └── Routes
        ├── DashboardPage.jsx
        │     ├── PageHeader
        │     ├── ConfidenceBar (per teks demo)
        │     └── RiskBadge (per teks demo)
        ├── PredictPage.jsx
        │     ├── PageHeader
        │     ├── RiskBadge
        │     ├── ConfidenceBar
        │     └── KeywordChips
        └── ConversationPage.jsx
              ├── PageHeader
              ├── RiskBadge (per pesan)
              ├── ConfidenceBar (per pesan)
              └── KeywordChips (per pesan)
```

---

*Dokumen ini dihasilkan dari pembacaan seluruh kode sumber proyek BullyGuard.*
