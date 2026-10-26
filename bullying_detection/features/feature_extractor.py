"""
Modul feature extraction untuk deteksi bullying.
Mengkombinasikan TF-IDF dan fitur leksikal (kata-kata kasar, ancaman, dll.)
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from scipy.sparse import hstack


# ============================================================
# LEXICON KATA BULLYING
# ============================================================

# Kata-kata kasar / makian
KATA_KASAR = {
    "anjing", "anjir", "anjay", "babi", "bangsat", "brengsek", "kampret",
    "sialan", "keparat", "bajingan", "kurang ajar", "goblok", "goblog",
    "bodoh", "tolol", "idiot", "bego", "dungu", "geblek", "bebal",
    "sampah", "tai", "taik", "bacot", "asu", "celeng", "bedebah",
    "setan", "iblis", "hantu", "monyet", "kera",
}

# Kata-kata ancaman
KATA_ANCAMAN = {
    "hajar", "pukul", "tonjok", "tampar", "tendang", "bunuh",
    "habisi", "laporin", "sebar", "sebarkan", "ancam", "intimidasi",
    "awas", "tunggu", "nyesel", "balas", "bakar", "hancur", "sikat",
    "gebuk", "bogem", "ajur", "remuk",
}

# Kata-kata pengucilan / isolasi
KATA_PENGUCILAN = {
    "pergi", "minggat", "enyah", "usir", "buang", "dibuang",
    "sendirian", "kesepian", "tidak diundang", "tidak diterima",
    "tidak disukai", "dibenci", "dikucilkan", "diisolasi",
    "tidak berteman", "tidak ada teman", "tidak ada yang mau",
}

# Kata-kata merendahkan / menghina
KATA_MERENDAHKAN = {
    "jelek", "buruk", "menjijikkan", "jorok", "kotor", "norak",
    "kampungan", "udik", "kuno", "ketinggalan", "miskin", "melarat",
    "gendut", "kurus", "pendek", "kerdil", "item", "hitam", "pesek",
    "jerawatan", "tidak berguna", "tidak penting", "sia-sia",
    "memalukan", "malu-maluin", "beban", "lemah", "loser",
    "gagal", "pecundang", "tidak bisa", "tidak mampu",
}

# Kata-kata penyebaran gosip / cyberbullying
KATA_GOSIP = {
    "screenshot", "sebar", "sebarkan", "bocorkan", "viral", "expose",
    "bocorin", "bongkar", "ungkap", "terbongkar", "rahasia",
    "gosip", "fitnah", "bohong", "dusta", "palsu", "tipu",
}

# Gabungan semua kata bullying
ALL_BULLYING_WORDS = (
    KATA_KASAR
    | KATA_ANCAMAN
    | KATA_PENGUCILAN
    | KATA_MERENDAHKAN
    | KATA_GOSIP
)


# ============================================================
# LEXICAL FEATURE EXTRACTOR
# ============================================================

class LexicalFeatureExtractor:
    """
    Mengekstrak fitur leksikal dari teks untuk deteksi bullying.
    Menghasilkan vektor numerik dari karakteristik teks.
    """

    def __init__(self):
        self.feature_names_ = [
            "jumlah_kata_kasar",
            "jumlah_kata_ancaman",
            "jumlah_kata_pengucilan",
            "jumlah_kata_merendahkan",
            "jumlah_kata_gosip",
            "rasio_kata_bullying",
            "panjang_teks",
            "jumlah_tanda_seru",
            "jumlah_huruf_kapital",
            "mengandung_ancaman_fisik",
            "mengandung_sebar_informasi",
        ]

    def _count_matches(self, text: str, word_set: set) -> int:
        """Hitung jumlah kata dari word_set yang muncul di teks."""
        tokens = text.lower().split()
        return sum(1 for t in tokens if t in word_set)

    def _ratio_bullying_words(self, text: str) -> float:
        """Hitung rasio kata bullying terhadap total kata."""
        tokens = text.lower().split()
        if not tokens:
            return 0.0
        count = sum(1 for t in tokens if t in ALL_BULLYING_WORDS)
        return count / len(tokens)

    def _count_exclamation(self, text: str) -> int:
        """Hitung jumlah tanda seru."""
        return text.count("!")

    def _count_uppercase(self, text: str) -> int:
        """Hitung jumlah huruf kapital (indikasi teriak)."""
        return sum(1 for c in text if c.isupper())

    def _has_physical_threat(self, text: str) -> int:
        """Apakah teks mengandung ancaman fisik? (0/1)"""
        physical = {"hajar", "pukul", "tonjok", "tampar", "tendang",
                    "bunuh", "habisi", "sikat", "gebuk", "bogem"}
        tokens = text.lower().split()
        return int(any(t in physical for t in tokens))

    def _has_spread_info(self, text: str) -> int:
        """Apakah teks mengandung ancaman sebar informasi? (0/1)"""
        spread = {"screenshot", "sebar", "sebarkan", "bocorkan",
                  "viral", "expose", "bocorin"}
        tokens = text.lower().split()
        return int(any(t in spread for t in tokens))

    def extract(self, text: str) -> np.ndarray:
        """
        Ekstrak semua fitur leksikal dari satu teks.

        Returns:
            numpy array dengan 11 fitur leksikal
        """
        # Simpan teks original untuk fitur non-preprocessed
        original = text

        features = np.array([
            self._count_matches(text, KATA_KASAR),
            self._count_matches(text, KATA_ANCAMAN),
            self._count_matches(text, KATA_PENGUCILAN),
            self._count_matches(text, KATA_MERENDAHKAN),
            self._count_matches(text, KATA_GOSIP),
            self._ratio_bullying_words(text),
            len(text.split()),                        # panjang teks (kata)
            self._count_exclamation(original),        # tanda seru
            self._count_uppercase(original),          # huruf kapital
            self._has_physical_threat(text),          # ancaman fisik
            self._has_spread_info(text),              # sebar informasi
        ], dtype=float)

        return features

    def extract_batch(self, texts: list) -> np.ndarray:
        """
        Ekstrak fitur leksikal untuk sekumpulan teks.

        Returns:
            numpy array shape (n_samples, 11)
        """
        return np.array([self.extract(t) for t in texts])

    def get_feature_names(self) -> list:
        """Mengembalikan nama-nama fitur."""
        return self.feature_names_


# ============================================================
# TFIDF + LEXICAL COMBINED EXTRACTOR
# ============================================================

class BullyingFeatureExtractor:
    """
    Menggabungkan TF-IDF dan fitur leksikal menjadi satu representasi fitur.
    """

    def __init__(
        self,
        tfidf_max_features: int = 5000,
        tfidf_ngram_range: tuple = (1, 2),
        tfidf_min_df: int = 1,
    ):
        self.tfidf = TfidfVectorizer(
            max_features=tfidf_max_features,
            ngram_range=tfidf_ngram_range,
            min_df=tfidf_min_df,
            sublinear_tf=True,  # log(1+tf) untuk mengurangi bias kata frekuensi tinggi
        )
        self.lexical = LexicalFeatureExtractor()
        self.is_fitted = False

    def fit(self, texts: list):
        """Fit TF-IDF pada data training."""
        self.tfidf.fit(texts)
        self.is_fitted = True
        return self

    def transform(self, texts: list):
        """
        Transform teks menjadi matriks fitur gabungan.

        Returns:
            scipy sparse matrix: (n_samples, tfidf_features + 11)
        """
        if not self.is_fitted:
            raise RuntimeError("Extractor belum di-fit. Panggil fit() terlebih dahulu.")

        tfidf_matrix = self.tfidf.transform(texts)
        lexical_matrix = self.lexical.extract_batch(texts)

        # Gabungkan TF-IDF (sparse) dengan lexical (dense) secara horizontal
        from scipy.sparse import csr_matrix
        combined = hstack([tfidf_matrix, csr_matrix(lexical_matrix)])
        return combined

    def fit_transform(self, texts: list):
        """Fit kemudian transform sekaligus."""
        self.fit(texts)
        return self.transform(texts)

    def get_feature_names(self) -> list:
        """Mengembalikan semua nama fitur."""
        tfidf_names = list(self.tfidf.get_feature_names_out())
        lex_names = self.lexical.get_feature_names()
        return tfidf_names + lex_names

    @property
    def n_features(self) -> int:
        """Jumlah total fitur."""
        if not self.is_fitted:
            return 0
        return len(self.tfidf.vocabulary_) + len(self.lexical.feature_names_)


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    from preprocessing.text_preprocessor import preprocess_batch

    contoh = [
        "dasar goblok banget sih lo, ga bisa apa-apa",
        "semangat ya, kamu pasti bisa lulus ujian itu",
        "awas lo ya, besok gue hajar abis-abisan!!!",
        "belajar bareng yuk, ujian minggu depan nih",
        "lo tuh sampah, ga ada yang mau temenan sama lo",
    ]

    # Preprocessing
    cleaned = preprocess_batch(contoh)

    # Ekstraksi fitur
    extractor = BullyingFeatureExtractor(tfidf_max_features=100)
    X = extractor.fit_transform(cleaned)

    print("=== Demo Feature Extraction ===\n")
    print(f"Jumlah sampel     : {X.shape[0]}")
    print(f"Jumlah fitur total: {X.shape[1]}")
    print(f"  - TF-IDF : {len(extractor.tfidf.vocabulary_)}")
    print(f"  - Lexical: {len(extractor.lexical.feature_names_)}")

    print("\n=== Fitur Leksikal ===")
    lex_extractor = LexicalFeatureExtractor()
    for teks, cleaned_teks in zip(contoh, cleaned):
        fitur = lex_extractor.extract(cleaned_teks)
        print(f"\nTeks: {teks[:50]}")
        for nama, nilai in zip(lex_extractor.get_feature_names(), fitur):
            if nilai > 0:
                print(f"  {nama}: {nilai:.2f}")
