"""
Modul preprocessing teks untuk deteksi bullying bahasa Indonesia.
Fungsi: cleaning, normalisasi, tokenisasi, hapus stopwords.
"""

import re
import string


# ============================================================
# STOPWORDS BAHASA INDONESIA
# ============================================================

STOPWORDS_ID = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan", "untuk",
    "pada", "adalah", "dalam", "tidak", "akan", "atau", "juga", "sudah",
    "saya", "aku", "kamu", "kita", "kami", "mereka", "dia", "ia",
    "ada", "lebih", "sangat", "apa", "siapa", "bagaimana", "mengapa",
    "karena", "jadi", "seperti", "kalau", "jika", "maka", "bisa", "bisa",
    "telah", "sedang", "masih", "belum", "pun", "pula", "lagi", "sudah",
    "agar", "supaya", "namun", "tetapi", "tapi", "namun", "namun",
    "ya", "yah", "yup", "iya", "ok", "oke", "deh", "dong", "sih",
    "lah", "kan", "nih", "nah", "tuh", "gitu", "gini", "aja",
    "banget", "bgt", "sekali", "paling", "sangat", "amat",
    "nya", "ku", "mu", "kah", "lah", "tah",
    "jangan", "tidak", "ga", "gak", "engga", "nggak", "tidak",
    "itu", "ini", "sini", "sana", "situ", "mana",
    "mau", "ingin", "minta", "tolong", "mohon",
    "harus", "perlu", "wajib", "boleh",
    "setelah", "sebelum", "ketika", "waktu", "saat",
    "di", "ke", "dari", "oleh", "tentang", "antara", "bagi",
    "sebagai", "karena", "sehingga", "agar", "supaya",
    "nya", "ber", "me", "di", "ter", "ke", "se",
    "lagi", "pernah", "selalu", "sering", "jarang", "biasa",
    "terus", "kemudian", "lalu", "tapi", "namun", "tetapi",
    "hingga", "sampai", "bahwa", "jika", "apabila",
}

# Kamus normalisasi slang → baku
SLANG_DICT = {
    # Kata slang umum
    "gw": "saya",
    "gue": "saya",
    "gua": "saya",
    "lo": "kamu",
    "lu": "kamu",
    "loe": "kamu",
    "lo": "kamu",
    "emg": "memang",
    "emang": "memang",
    "gmn": "bagaimana",
    "gimana": "bagaimana",
    "knp": "kenapa",
    "krn": "karena",
    "karna": "karena",
    "yg": "yang",
    "dgn": "dengan",
    "utk": "untuk",
    "buat": "untuk",
    "sm": "sama",
    "jg": "juga",
    "tp": "tapi",
    "tpi": "tapi",
    "ttg": "tentang",
    "kpd": "kepada",
    "dr": "dari",
    "hrs": "harus",
    "msh": "masih",
    "sdh": "sudah",
    "udah": "sudah",
    "udh": "sudah",
    "blm": "belum",
    "belom": "belum",
    "kyk": "seperti",
    "kayak": "seperti",
    "bkn": "bukan",
    "bukan": "bukan",
    "bngt": "banget",
    "bgt": "banget",
    "abis": "habis",
    "abiss": "habis",
    "ges": "semuanya",
    "gais": "semuanya",
    "guys": "semuanya",
    "cuy": "kawan",
    "bro": "kawan",
    "sis": "kawan",
    "sist": "kawan",
    "gan": "kawan",
    "bray": "kawan",
    "banh": "kawan",
    "wkwk": "",
    "haha": "",
    "hehe": "",
    "hihi": "",
    "huhu": "",
    "lol": "",
    "lmao": "",
    "omg": "",
    "wtf": "",
    "anjir": "anjing",
    "anjay": "anjing",
    "jir": "anjing",
    "babi": "babi",
    "kampret": "kampret",
    "brengsek": "brengsek",
    "bangsat": "bangsat",
    "goblok": "bodoh",
    "goblog": "bodoh",
    "tolol": "bodoh",
    "idiot": "bodoh",
    "bego": "bodoh",
    "bodoh": "bodoh",
    "geblek": "bodoh",
    "bapack": "bapack",
    "ngga": "tidak",
    "nggak": "tidak",
    "gak": "tidak",
    "ga": "tidak",
    "tdk": "tidak",
    "nope": "tidak",
    "yoi": "ya",
    "yep": "ya",
    "iyap": "ya",
    "enak": "enak",
    "asik": "asyik",
    "asyik": "asyik",
    "keren": "bagus",
    "mantap": "bagus",
    "mantul": "bagus",
    "manteb": "bagus",
    "kuy": "ayo",
    "yuk": "ayo",
    "mari": "ayo",
    "mksd": "maksud",
    "maksudnya": "maksud",
    "mksdt": "maksud",
    "ktnya": "katanya",
    "org": "orang",
    "orng": "orang",
    "tman": "teman",
    "tmn": "teman",
    "smua": "semua",
    "semuanya": "semua",
    "plg": "paling",
    "bgt": "banget",
    "blg": "bilang",
    "blng": "bilang",
    "dtg": "datang",
    "prgi": "pergi",
    "pergi": "pergi",
    "ngmng": "ngomong",
    "ngomong": "bicara",
    "bilang": "bicara",
    "crita": "cerita",
    "cerita": "cerita",
    "chat": "pesan",
    "msg": "pesan",
    "dm": "pesan",
    "info": "informasi",
    "minta": "minta",
    "mnta": "minta",
    "makasih": "terima kasih",
    "thx": "terima kasih",
    "thanks": "terima kasih",
    "sory": "maaf",
    "sorry": "maaf",
    "maaf": "maaf",
    "maf": "maaf",
}


# ============================================================
# FUNGSI PREPROCESSING
# ============================================================

def lowercase(text: str) -> str:
    """Ubah teks ke huruf kecil."""
    return text.lower()


def remove_url(text: str) -> str:
    """Hapus URL dari teks."""
    return re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)


def remove_mentions_hashtags(text: str) -> str:
    """Hapus mention (@user) dan hashtag (#tag)."""
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    return text


def remove_emoji(text: str) -> str:
    """Hapus emoji dan karakter unicode non-standar."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def remove_punctuation(text: str) -> str:
    """Hapus tanda baca."""
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_numbers(text: str) -> str:
    """Hapus angka dari teks."""
    return re.sub(r"\d+", "", text)


def remove_extra_whitespace(text: str) -> str:
    """Hapus spasi berlebih."""
    return re.sub(r"\s+", " ", text).strip()


def normalize_repeated_chars(text: str) -> str:
    """Normalisasi karakter berulang: 'goblooook' → 'goblok'."""
    return re.sub(r"(.)\1{2,}", r"\1\1", text)


def normalize_slang(text: str) -> str:
    """Ganti kata slang dengan padanan bakunya."""
    tokens = text.split()
    normalized = [SLANG_DICT.get(token, token) for token in tokens]
    # Hapus token kosong (dari slang yang dibuang)
    normalized = [t for t in normalized if t.strip()]
    return " ".join(normalized)


def tokenize(text: str) -> list:
    """Tokenisasi sederhana berdasarkan spasi."""
    return text.split()


def remove_stopwords(tokens: list) -> list:
    """Hapus stopwords dari daftar token."""
    return [t for t in tokens if t not in STOPWORDS_ID]


def preprocess(text: str, remove_stop: bool = True) -> str:
    """
    Pipeline preprocessing lengkap.

    Args:
        text: teks mentah
        remove_stop: apakah stopwords dihapus (default True)

    Returns:
        Teks yang sudah diproses
    """
    text = lowercase(text)
    text = remove_url(text)
    text = remove_mentions_hashtags(text)
    text = remove_emoji(text)
    text = normalize_repeated_chars(text)
    text = normalize_slang(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    text = remove_extra_whitespace(text)

    if remove_stop:
        tokens = tokenize(text)
        tokens = remove_stopwords(tokens)
        text = " ".join(tokens)

    return text


def preprocess_batch(texts: list, remove_stop: bool = True) -> list:
    """
    Preprocessing untuk sekumpulan teks.

    Args:
        texts: list teks mentah
        remove_stop: apakah stopwords dihapus

    Returns:
        List teks yang sudah diproses
    """
    return [preprocess(t, remove_stop) for t in texts]


# ============================================================
# TEST / DEMO
# ============================================================

if __name__ == "__main__":
    contoh = [
        "dasar GOBLOK banget sih lo!! ga bisa apa-apa 😤",
        "hei, apa kabar? sudah lama ga ketemu nih :)",
        "awas lo ya!!! besok gw hajar lo abis-abisan!!!",
        "makasih udah bantuin aku tadi, baik banget deh",
        "idiiiiiot bgt lo, malu-maluin aja",
    ]

    print("=== Demo Preprocessing ===\n")
    for teks in contoh:
        hasil = preprocess(teks)
        print(f"  Input : {teks}")
        print(f"  Output: {hasil}")
        print()
