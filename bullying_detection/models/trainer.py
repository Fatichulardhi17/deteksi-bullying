"""
Modul training dan evaluasi model ML untuk deteksi bullying.
Model yang dibandingkan: Naive Bayes, Logistic Regression, SVM, Random Forest.
"""

import os
import pickle
import numpy as np
import pandas as pd

from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import MaxAbsScaler


# ============================================================
# KONFIGURASI MODEL
# ============================================================

MODEL_CONFIG = {
    "naive_bayes": {
        "model": ComplementNB(alpha=0.5),
        "description": "Complement Naive Bayes (cocok untuk teks)",
    },
    "logistic_regression": {
        "model": LogisticRegression(
            C=1.0,
            max_iter=1000,
            random_state=42,
            class_weight="balanced",
        ),
        "description": "Logistic Regression",
    },
    "svm": {
        "model": CalibratedClassifierCV(
            LinearSVC(C=1.0, max_iter=2000, random_state=42, class_weight="balanced"),
            cv=3,
        ),
        "description": "Support Vector Machine (LinearSVC + Calibration)",
    },
    "random_forest": {
        "model": RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        ),
        "description": "Random Forest",
    },
}


# ============================================================
# TRAINER
# ============================================================

class BullyingModelTrainer:
    """
    Melatih dan mengevaluasi model ML untuk deteksi bullying.
    """

    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        self.test_size = test_size
        self.random_state = random_state
        self.trained_models = {}
        self.results = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.best_model_name = None
        self.best_model = None
        self.scaler = MaxAbsScaler()  # Cocok untuk sparse matrix

    def split_data(self, X, y):
        """Bagi data menjadi train/test dengan stratified split."""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y,
        )
        print(f"Split data: {len(self.y_train)} train | {len(self.y_test)} test")
        print(f"  Train — Bullying: {sum(self.y_train)} | Non-Bullying: {len(self.y_train) - sum(self.y_train)}")
        print(f"  Test  — Bullying: {sum(self.y_test)} | Non-Bullying: {len(self.y_test) - sum(self.y_test)}")
        return self.X_train, self.X_test, self.y_train, self.y_test

    def scale_features(self, fit: bool = True):
        """
        Scaling fitur (MaxAbsScaler, aman untuk sparse matrix).
        Hanya fit pada data train untuk menghindari data leakage.
        """
        if fit:
            self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        return self.X_train, self.X_test

    def train_single(self, model_name: str, X_train=None, y_train=None):
        """Melatih satu model."""
        if model_name not in MODEL_CONFIG:
            raise ValueError(f"Model '{model_name}' tidak ditemukan. Pilih: {list(MODEL_CONFIG.keys())}")

        X = X_train if X_train is not None else self.X_train
        y = y_train if y_train is not None else self.y_train

        config = MODEL_CONFIG[model_name]
        model = config["model"]

        print(f"  Melatih {config['description']}...", end=" ")
        model.fit(X, y)
        self.trained_models[model_name] = model
        print("✓")

        return model

    def train_all(self, X_train=None, y_train=None):
        """Melatih semua model sekaligus."""
        print("\n=== Training Semua Model ===")
        for name in MODEL_CONFIG:
            self.train_single(name, X_train, y_train)
        print(f"  {len(self.trained_models)} model berhasil dilatih.\n")
        return self.trained_models

    def evaluate_single(self, model_name: str, X_test=None, y_test=None) -> dict:
        """
        Mengevaluasi satu model dan mengembalikan metrik.

        Returns:
            dict berisi accuracy, precision, recall, f1, auc
        """
        if model_name not in self.trained_models:
            raise ValueError(f"Model '{model_name}' belum dilatih.")

        X = X_test if X_test is not None else self.X_test
        y = y_test if y_test is not None else self.y_test

        model = self.trained_models[model_name]
        y_pred = model.predict(X)

        # Probabilitas untuk AUC (jika tersedia)
        auc = None
        try:
            y_prob = model.predict_proba(X)[:, 1]
            auc = roc_auc_score(y, y_prob)
        except AttributeError:
            pass

        result = {
            "model_name": model_name,
            "description": MODEL_CONFIG[model_name]["description"],
            "accuracy": accuracy_score(y, y_pred),
            "precision": precision_score(y, y_pred, zero_division=0),
            "recall": recall_score(y, y_pred, zero_division=0),
            "f1_score": f1_score(y, y_pred, zero_division=0),
            "auc_roc": auc,
            "confusion_matrix": confusion_matrix(y, y_pred),
            "classification_report": classification_report(
                y, y_pred,
                target_names=["Non-Bullying", "Bullying"],
                zero_division=0,
            ),
            "y_pred": y_pred,
        }

        self.results[model_name] = result
        return result

    def evaluate_all(self, X_test=None, y_test=None) -> dict:
        """Evaluasi semua model yang sudah dilatih."""
        print("=== Evaluasi Semua Model ===\n")
        for name in self.trained_models:
            self.evaluate_single(name, X_test, y_test)
        return self.results

    def cross_validate(self, model_name: str, X, y, cv: int = 5) -> dict:
        """
        Cross-validation pada seluruh dataset.

        Args:
            model_name: nama model
            X: fitur
            y: label
            cv: jumlah fold

        Returns:
            dict berisi mean dan std tiap metrik
        """
        if model_name not in MODEL_CONFIG:
            raise ValueError(f"Model '{model_name}' tidak ditemukan.")

        # Buat instance baru agar tidak mengubah state model yg sudah dilatih
        model = MODEL_CONFIG[model_name]["model"]
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)

        metrics = {}
        for metric in ["accuracy", "f1", "precision", "recall"]:
            scoring = metric if metric != "f1" else "f1"
            scores = cross_val_score(model, X, y, cv=skf, scoring=scoring)
            metrics[metric] = {"mean": scores.mean(), "std": scores.std()}

        return metrics

    def get_comparison_table(self) -> pd.DataFrame:
        """
        Membuat tabel perbandingan semua model.

        Returns:
            pandas DataFrame dengan metrik tiap model
        """
        if not self.results:
            raise RuntimeError("Belum ada hasil evaluasi. Panggil evaluate_all() terlebih dahulu.")

        rows = []
        for name, res in self.results.items():
            rows.append({
                "Model": res["description"],
                "Accuracy": f"{res['accuracy']:.4f}",
                "Precision": f"{res['precision']:.4f}",
                "Recall": f"{res['recall']:.4f}",
                "F1-Score": f"{res['f1_score']:.4f}",
                "AUC-ROC": f"{res['auc_roc']:.4f}" if res["auc_roc"] else "N/A",
            })

        df = pd.DataFrame(rows)
        return df

    def select_best_model(self, metric: str = "f1_score") -> tuple:
        """
        Pilih model terbaik berdasarkan metrik tertentu.

        Args:
            metric: 'accuracy', 'f1_score', 'precision', 'recall', 'auc_roc'

        Returns:
            (nama_model, model_object)
        """
        if not self.results:
            raise RuntimeError("Belum ada hasil evaluasi.")

        best_name = max(
            self.results,
            key=lambda name: self.results[name].get(metric) or 0
        )
        self.best_model_name = best_name
        self.best_model = self.trained_models[best_name]

        print(f"\nModel terbaik (berdasarkan {metric}): {best_name}")
        print(f"  {metric}: {self.results[best_name].get(metric):.4f}")

        return best_name, self.best_model

    def print_results(self):
        """Cetak hasil evaluasi semua model ke konsol."""
        print("\n" + "=" * 65)
        print("HASIL EVALUASI MODEL")
        print("=" * 65)

        for name, res in self.results.items():
            print(f"\n{'─' * 50}")
            print(f"Model : {res['description']}")
            print(f"{'─' * 50}")
            print(f"  Accuracy  : {res['accuracy']:.4f}")
            print(f"  Precision : {res['precision']:.4f}")
            print(f"  Recall    : {res['recall']:.4f}")
            print(f"  F1-Score  : {res['f1_score']:.4f}")
            if res["auc_roc"]:
                print(f"  AUC-ROC   : {res['auc_roc']:.4f}")
            print(f"\n  Classification Report:")
            print(res["classification_report"])
            print(f"  Confusion Matrix:")
            cm = res["confusion_matrix"]
            print(f"    TN={cm[0][0]} | FP={cm[0][1]}")
            print(f"    FN={cm[1][0]} | TP={cm[1][1]}")

        print("\n" + "=" * 65)
        print("TABEL PERBANDINGAN")
        print("=" * 65)
        print(self.get_comparison_table().to_string(index=False))
        print("=" * 65)

    def save_model(self, model_name: str, filepath: str):
        """Simpan model ke file pickle."""
        if model_name not in self.trained_models:
            raise ValueError(f"Model '{model_name}' belum dilatih.")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self.trained_models[model_name], f)
        print(f"  Model '{model_name}' disimpan ke: {filepath}")

    def save_scaler(self, filepath: str):
        """Simpan scaler ke file pickle."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self.scaler, f)
        print(f"  Scaler disimpan ke: {filepath}")


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    from data.dataset import get_dataframe
    from preprocessing.text_preprocessor import preprocess_batch
    from features.feature_extractor import BullyingFeatureExtractor

    # Load & preprocess data
    print("Memuat dataset...")
    df = get_dataframe()
    texts_clean = preprocess_batch(df["text"].tolist())
    labels = df["label"].tolist()

    # Ekstraksi fitur
    print("Mengekstrak fitur...")
    extractor = BullyingFeatureExtractor(tfidf_max_features=3000)
    X = extractor.fit_transform(texts_clean)
    y = np.array(labels)

    # Training & evaluasi
    trainer = BullyingModelTrainer(test_size=0.2, random_state=42)
    trainer.split_data(X, y)
    trainer.scale_features()

    trainer.train_all()
    trainer.evaluate_all()
    trainer.print_results()
    trainer.select_best_model(metric="f1_score")
