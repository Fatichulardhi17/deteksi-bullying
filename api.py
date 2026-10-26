"""
Backend API Flask untuk sistem deteksi bullying.
Expose endpoint untuk prediksi individual, batch, dan analisis percakapan.
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Tambahkan root direktori ke path
sys.path.insert(0, os.path.dirname(__file__))

from bullying_detection.inference.detector import BullyingDetector

app = Flask(__name__)
CORS(app)  # Izinkan akses dari React frontend

# ─────────────────────────────────────────
# Inisialisasi model
# ─────────────────────────────────────────

detector = BullyingDetector()
MODEL_DIR = os.path.join(os.path.dirname(__file__), "bullying_detection", "saved_model")

try:
    detector.load(MODEL_DIR)
    print("[API] Model berhasil dimuat.")
except Exception as e:
    print(f"[API] Gagal memuat model: {e}")
    print("[API] Melatih model baru...")
    detector.train(model_name="logistic_regression", save_dir=MODEL_DIR)


# ─────────────────────────────────────────
# Helper
# ─────────────────────────────────────────

def prediction_to_dict(result) -> dict:
    """Konversi PredictionResult ke dict JSON-serializable."""
    return {
        "text_original": result.text_original,
        "text_processed": result.text_processed,
        "label": result.label,
        "label_str": result.label_str,
        "confidence": round(result.confidence, 4),
        "confidence_bullying": round(result.confidence_bullying, 4),
        "confidence_non_bullying": round(result.confidence_non_bullying, 4),
        "risk_level": result.risk_level,
        "detected_keywords": result.detected_keywords,
        "lexical_features": result.lexical_features,
        "warning_message": result.warning_message,
    }


# ─────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "Bullying Detection API",
        "version": "1.0.0",
        "endpoints": [
            "POST /predict        - Prediksi satu teks",
            "POST /predict/batch  - Prediksi banyak teks",
            "POST /analyze        - Analisis percakapan",
            "GET  /health         - Status API",
        ]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model_ready": detector.is_ready,
        "model_name": detector.model_name,
    })


@app.route("/predict", methods=["POST"])
def predict():
    """
    Prediksi satu teks.

    Request body:
        { "text": "teks yang ingin diprediksi" }

    Response:
        PredictionResult sebagai JSON
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Field 'text' diperlukan"}), 400

    text = str(data["text"]).strip()
    if not text:
        return jsonify({"error": "Teks tidak boleh kosong"}), 400

    try:
        result = detector.predict(text)
        return jsonify(prediction_to_dict(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict/batch", methods=["POST"])
def predict_batch():
    """
    Prediksi banyak teks sekaligus.

    Request body:
        { "texts": ["teks1", "teks2", ...] }

    Response:
        BatchPredictionResult sebagai JSON
    """
    data = request.get_json()
    if not data or "texts" not in data:
        return jsonify({"error": "Field 'texts' (array) diperlukan"}), 400

    texts = data["texts"]
    if not isinstance(texts, list) or len(texts) == 0:
        return jsonify({"error": "'texts' harus berupa array tidak kosong"}), 400

    if len(texts) > 100:
        return jsonify({"error": "Maksimal 100 teks per request"}), 400

    try:
        batch_result = detector.predict_batch(texts)
        return jsonify({
            "total": batch_result.total,
            "n_bullying": batch_result.n_bullying,
            "n_non_bullying": batch_result.n_non_bullying,
            "bullying_ratio": round(batch_result.bullying_ratio, 4),
            "predictions": [prediction_to_dict(p) for p in batch_result.predictions],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze", methods=["POST"])
def analyze_conversation():
    """
    Analisis percakapan (list pesan berurutan).

    Request body:
        {
            "messages": [
                { "sender": "Alice", "text": "..." },
                ...
            ]
        }

    Response:
        Hasil analisis percakapan sebagai JSON
    """
    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"error": "Field 'messages' (array) diperlukan"}), 400

    messages = data["messages"]
    if not isinstance(messages, list) or len(messages) == 0:
        return jsonify({"error": "'messages' harus berupa array tidak kosong"}), 400

    if len(messages) > 200:
        return jsonify({"error": "Maksimal 200 pesan per request"}), 400

    # Validasi format pesan
    for i, msg in enumerate(messages):
        if not isinstance(msg, dict) or "text" not in msg:
            return jsonify({"error": f"Pesan ke-{i} harus memiliki field 'text'"}), 400
        if "sender" not in msg:
            messages[i]["sender"] = f"User{i+1}"

    try:
        result = detector.analyze_conversation(messages)

        # Tambahkan detail prediksi per pesan
        detailed_messages = []
        for msg in messages:
            pred = detector.predict(msg["text"])
            detailed_messages.append({
                "sender": msg.get("sender", "Unknown"),
                "text": msg["text"],
                "prediction": prediction_to_dict(pred),
            })

        result["detailed_messages"] = detailed_messages
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  Bullying Detection API")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
