"""
Modul inference untuk prediksi bullying pada chat baru secara real-time.
Menyediakan kelas BullyingDetector sebagai interface utama sistem.
"""

import pickle
import os
import sys
import numpy as np
from dataclasses import dataclass, field
from typing import Optional

# Tambahkan root direktori ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from preprocessing.text_preprocessor import preprocess
from features.feature_extractor import BullyingFeatureExtractor, LexicalFeatureExtractor


# ============================================================
# DATA CLASS HASIL PREDIKSI
# ============================================================

@dataclass
class PredictionResult:
    """Hasil prediksi satu teks chat."""
    text_original: str
    text_processed: str
    label: int                         # 0 = tidak bullying, 1 = bullying
    label_str: str                     # "Bullying" / "Tidak Bullying"
    confidence: float                  # probabilitas kelas prediksi (0–1)
    confidence_bullying: float         # probabilitas bullying
    confidence_non_bullying: float     # probabilitas tidak bullying
    risk_level: str                    # "Rendah" / "Sedang" / "Tinggi"
    detected_keywords: list = field(default_factory=list)
    lexical_features: dict = field(default_factory=dict)
    warning_message: Optional[str] = None

    def __str__(self) -> str:
        lines = [
            "┌─────────────────────────────────────────────────────┐",
            f"│ Teks     : {self.text_original[:48]:<48} │",
            f"│ Status   : {'⚠️  ' + self.label_str if self.label == 1 else '✅  ' + self.label_str:<49} │",
            f"│ Risk     : {self.risk_level:<49} │",
            f"│ Conf     : {self.confidence:.2%} (Bullying: {self.confidence_bullying:.2%}, Non: {self.confidence_non_bullying:.2%})",
        ]
        if self.detected_keywords:
            kw = ", ".join(self.detected_keywords[:5])
            lines.append(f"│ Keywords : {kw[:48]:<48} │")
        if self.warning_message:
            lines.append(f"│ ⚠️  {self.warning_message[:52]:<52} │")
        lines.append("└─────────────────────────────────────────────────────┘")
        return "\n".join(lines)


@dataclass
class BatchPredictionResult:
    """Hasil prediksi sekumpulan teks chat."""
    predictions: list
    total: int
    n_bullying: int
    n_non_bullying: int
    bullying_ratio: float

    def summary(self) -> str:
        return (
            f"\n=== Ringkasan Analisis ===\n"
            f"  Total chat         : {self.total}\n"
            f"  Terdeteksi bullying: {self.n_bullying} ({self.bullying_ratio:.1%})\n"
            f"  Aman               : {self.n_non_bullying} ({1 - self.bullying_ratio:.1%})\n"
        )


# ============================================================
# BULLYING DETECTOR
# ============================================================

class BullyingDetector:
    """
    Interface utama sistem deteksi bullying.

    Penggunaan:
        detector = BullyingDetector()
        detector.train()                     # atau load model yang sudah ada
        result = detector.predict("teks chat")
    """

    def __init__(self):
        self.extractor = BullyingFeatureExtractor(tfidf_max_features=3000)
        self.lexical = LexicalFeatureExtractor()
        self.model = None
        self.scaler = None
        self.model_name = None
        self.is_ready = False

    # ─────────────────────────────────────────
    # SETUP
    # ─────────────────────────────────────────

    def train(
        self,
        df=None,
        model_name: str = "logistic_regression",
        save_dir: Optional[str] = None,
    ):
        """
        Melatih model dari dataset.

        Args:
            df: pandas DataFrame dengan kolom 'text' dan 'label'.
                Jika None, load dari dataset bawaan.
            model_name: model yang digunakan ('naive_bayes', 'logistic_regression',
                        'svm', 'random_forest')
            save_dir: direktori untuk menyimpan model (opsional)
        """
        from data.dataset import get_dataframe
        from preprocessing.text_preprocessor import preprocess_batch
        from models.trainer import BullyingModelTrainer

        if df is None:
            df = get_dataframe()

        print(f"[BullyingDetector] Melatih model: {model_name}...")

        # Preprocessing
        texts_clean = preprocess_batch(df["text"].tolist())
        labels = np.array(df["label"].tolist())

        # Fitur
        X = self.extractor.fit_transform(texts_clean)

        # Training
        trainer = BullyingModelTrainer()
        trainer.split_data(X, labels)
        trainer.scale_features(fit=True)
        self.scaler = trainer.scaler
        trainer.train_single(model_name, trainer.X_train, trainer.y_train)
        trainer.evaluate_single(model_name, trainer.X_test, trainer.y_test)

        self.model = trainer.trained_models[model_name]
        self.model_name = model_name
        self.is_ready = True

        # Simpan jika diminta
        if save_dir:
            self.save(save_dir)

        print(f"[BullyingDetector] Model siap digunakan.\n")
        return trainer.results[model_name]

    def save(self, save_dir: str):
        """Simpan model, extractor, dan scaler ke disk."""
        os.makedirs(save_dir, exist_ok=True)

        with open(os.path.join(save_dir, "model.pkl"), "wb") as f:
            pickle.dump(self.model, f)

        with open(os.path.join(save_dir, "extractor.pkl"), "wb") as f:
            pickle.dump(self.extractor, f)

        if self.scaler:
            with open(os.path.join(save_dir, "scaler.pkl"), "wb") as f:
                pickle.dump(self.scaler, f)

        print(f"[BullyingDetector] Model disimpan ke: {save_dir}")

    def load(self, save_dir: str):
        """Load model dari disk."""
        model_path = os.path.join(save_dir, "model.pkl")
        extractor_path = os.path.join(save_dir, "extractor.pkl")
        scaler_path = os.path.join(save_dir, "scaler.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model tidak ditemukan: {model_path}")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        with open(extractor_path, "rb") as f:
            self.extractor = pickle.load(f)

        if os.path.exists(scaler_path):
            with open(scaler_path, "rb") as f:
                self.scaler = pickle.load(f)

        self.is_ready = True
        print(f"[BullyingDetector] Model berhasil dimuat dari: {save_dir}")

    # ─────────────────────────────────────────
    # PREDIKSI
    # ─────────────────────────────────────────

    def _get_risk_level(self, prob_bullying: float) -> str:
        """Tentukan level risiko berdasarkan probabilitas."""
        if prob_bullying >= 0.7:
            return "🔴 Tinggi"
        elif prob_bullying >= 0.4:
            return "🟡 Sedang"
        else:
            return "🟢 Rendah"

    def _get_warning(self, result: "PredictionResult") -> Optional[str]:
        """Buat pesan peringatan jika diperlukan."""
        if result.label == 1:
            if result.risk_level.startswith("🔴"):
                return "Konten ini berpotensi menyebabkan trauma psikologis."
            elif result.risk_level.startswith("🟡"):
                return "Konten mengandung indikasi perundungan. Perlu dimoderasi."
        return None

    def _detect_keywords(self, text: str) -> list:
        """Deteksi kata kunci bullying yang muncul dalam teks."""
        from features.feature_extractor import ALL_BULLYING_WORDS
        tokens = text.lower().split()
        found = [t for t in tokens if t in ALL_BULLYING_WORDS]
        return list(set(found))

    def _build_lexical_info(self, text_processed: str) -> dict:
        """Bangun info fitur leksikal untuk ditampilkan."""
        features = self.lexical.extract(text_processed)
        names = self.lexical.get_feature_names()
        return {
            name: val
            for name, val in zip(names, features)
            if val > 0
        }

    def predict(self, text: str) -> PredictionResult:
        """
        Prediksi apakah satu teks chat mengandung bullying.

        Args:
            text: teks chat mentah

        Returns:
            PredictionResult
        """
        if not self.is_ready:
            raise RuntimeError("Detector belum siap. Panggil train() atau load() terlebih dahulu.")

        if not text or not text.strip():
            return PredictionResult(
                text_original=text,
                text_processed="",
                label=0,
                label_str="Tidak Bullying",
                confidence=1.0,
                confidence_bullying=0.0,
                confidence_non_bullying=1.0,
                risk_level="🟢 Rendah",
                warning_message=None,
            )

        # Preprocessing
        text_clean = preprocess(text)

        # Ekstraksi fitur
        X = self.extractor.transform([text_clean])
        if self.scaler:
            X = self.scaler.transform(X)

        # Prediksi
        label = int(self.model.predict(X)[0])

        # Probabilitas
        try:
            proba = self.model.predict_proba(X)[0]
            conf_non_bully = float(proba[0])
            conf_bully = float(proba[1])
        except AttributeError:
            conf_bully = 1.0 if label == 1 else 0.0
            conf_non_bully = 1.0 - conf_bully

        confidence = conf_bully if label == 1 else conf_non_bully
        label_str = "⚠️ Bullying" if label == 1 else "✅ Tidak Bullying"
        risk_level = self._get_risk_level(conf_bully)

        # Keyword & lexical
        keywords = self._detect_keywords(text_clean)
        lexical_info = self._build_lexical_info(text_clean)

        result = PredictionResult(
            text_original=text,
            text_processed=text_clean,
            label=label,
            label_str=label_str,
            confidence=confidence,
            confidence_bullying=conf_bully,
            confidence_non_bullying=conf_non_bully,
            risk_level=risk_level,
            detected_keywords=keywords,
            lexical_features=lexical_info,
        )
        result.warning_message = self._get_warning(result)
        return result

    def predict_batch(self, texts: list) -> BatchPredictionResult:
        """
        Prediksi sekumpulan teks chat sekaligus.

        Args:
            texts: list teks chat

        Returns:
            BatchPredictionResult
        """
        if not self.is_ready:
            raise RuntimeError("Detector belum siap.")

        predictions = [self.predict(t) for t in texts]
        n_bullying = sum(1 for p in predictions if p.label == 1)
        n_non = len(predictions) - n_bullying

        return BatchPredictionResult(
            predictions=predictions,
            total=len(predictions),
            n_bullying=n_bullying,
            n_non_bullying=n_non,
            bullying_ratio=n_bullying / len(predictions) if predictions else 0.0,
        )

    def analyze_conversation(self, messages: list) -> dict:
        """
        Analisis percakapan (list pesan berurutan).

        Args:
            messages: list dict dengan format:
                      [{"sender": "Alice", "text": "..."}, ...]

        Returns:
            dict berisi analisis per pengirim + ringkasan keseluruhan
        """
        sender_stats = {}
        flagged_messages = []

        for msg in messages:
            sender = msg.get("sender", "Unknown")
            text = msg.get("text", "")

            result = self.predict(text)

            if sender not in sender_stats:
                sender_stats[sender] = {
                    "total_pesan": 0,
                    "pesan_bullying": 0,
                    "risk_score": 0.0,
                }

            sender_stats[sender]["total_pesan"] += 1
            sender_stats[sender]["risk_score"] += result.confidence_bullying

            if result.label == 1:
                sender_stats[sender]["pesan_bullying"] += 1
                flagged_messages.append({
                    "sender": sender,
                    "text": text,
                    "risk_level": result.risk_level,
                    "keywords": result.detected_keywords,
                })

        # Hitung rata-rata risk score
        for sender, stats in sender_stats.items():
            if stats["total_pesan"] > 0:
                stats["avg_risk_score"] = stats["risk_score"] / stats["total_pesan"]
            del stats["risk_score"]

        total_pesan = len(messages)
        total_bullying = sum(s["pesan_bullying"] for s in sender_stats.values())

        return {
            "total_pesan": total_pesan,
            "total_bullying": total_bullying,
            "bullying_ratio": total_bullying / total_pesan if total_pesan else 0,
            "sender_stats": sender_stats,
            "flagged_messages": flagged_messages,
            "status": "⚠️ PERLU TINDAKAN" if total_bullying > 0 else "✅ AMAN",
        }


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    detector = BullyingDetector()
    detector.train(model_name="logistic_regression")

    print("\n" + "=" * 60)
    print("DEMO PREDIKSI INDIVIDUAL")
    print("=" * 60)

    uji_coba = [
        "dasar goblok, ga bisa ngerjain soal gampang aja",
        "semangat ya ujiannya, pasti bisa kok!",
        "awas lo ya, besok gue hajar habis-habisan!",
        "kita belajar bareng yuk buat persiapan ujian",
        "lo tuh ga ada gunanya, semua orang benci sama lo",
        "makasih udah bantuin aku tadi, baik banget",
    ]

    for teks in uji_coba:
        result = detector.predict(teks)
        print(f"\n🔎 Teks: \"{teks}\"")
        print(f"   Status  : {result.label_str}")
        print(f"   Risk    : {result.risk_level}")
        print(f"   P(bully): {result.confidence_bullying:.2%}")
        if result.detected_keywords:
            print(f"   Keyword : {result.detected_keywords}")

    print("\n" + "=" * 60)
    print("DEMO ANALISIS PERCAKAPAN")
    print("=" * 60)

    conversation = [
        {"sender": "Budi", "text": "hei, lo tuh bego banget sih!"},
        {"sender": "Siti", "text": "aku ga ngerti maksudmu"},
        {"sender": "Budi", "text": "dasar tolol, malu-maluin aja"},
        {"sender": "Siti", "text": "tolong jangan kasar dong"},
        {"sender": "Andi", "text": "udah, kalian berdamai aja yuk"},
        {"sender": "Budi", "text": "awas lo ya, besok ketemu gue hajar"},
    ]

    analisis = detector.analyze_conversation(conversation)

    print(f"\nStatus Percakapan : {analisis['status']}")
    print(f"Total pesan       : {analisis['total_pesan']}")
    print(f"Pesan bullying    : {analisis['total_bullying']} ({analisis['bullying_ratio']:.1%})")
    print("\nStatistik per pengirim:")
    for sender, stats in analisis["sender_stats"].items():
        print(f"  {sender}: {stats['pesan_bullying']}/{stats['total_pesan']} bullying | avg_risk={stats['avg_risk_score']:.2f}")
    print("\nPesan yang ditandai:")
    for msg in analisis["flagged_messages"]:
        print(f"  [{msg['risk_level']}] {msg['sender']}: \"{msg['text'][:50]}\"")
        if msg["keywords"]:
            print(f"    Keywords: {msg['keywords']}")
