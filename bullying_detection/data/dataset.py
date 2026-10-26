"""
Dataset sample untuk sistem deteksi bullying dalam chat bahasa Indonesia.
Label: 1 = bullying, 0 = tidak bullying
"""

DATASET = [
    # ============================================================
    # BULLYING (label = 1)
    # ============================================================

    # Hinaan fisik
    {"text": "dasar jelek banget muka lo, kayak hantu", "label": 1},
    {"text": "lo tuh gendut banget sih, babi aja kalah", "label": 1},
    {"text": "item banget lo, jorok deh liat mukanya", "label": 1},
    {"text": "kurus kering lo tuh makan dong jangan pelit", "label": 1},
    {"text": "pendek banget sih lo, kerdil emang", "label": 1},

    # Hinaan kecerdasan
    {"text": "bego banget sih lo, ga bisa apa-apa", "label": 1},
    {"text": "dasar idiot, soal gampang aja ga bisa", "label": 1},
    {"text": "otak lo isi apa? kapas ya? makanya bodoh terus", "label": 1},
    {"text": "lo tuh emang paling tolol di kelas", "label": 1},
    {"text": "ngapain sekolah kalo otaknya mampet kayak gitu", "label": 1},

    # Ancaman
    {"text": "awas lo ya, besok ketemu aku hajar", "label": 1},
    {"text": "lo bakal nyesel udah berani sama gue", "label": 1},
    {"text": "tunggu aja, gue bakal bikin lo nangis", "label": 1},
    {"text": "berani banget lo ya, mau gue laporin ke anak-anak", "label": 1},
    {"text": "sekali lagi lo ngomong gitu, habis lo sama gue", "label": 1},

    # Pengucilan / isolasi sosial
    {"text": "ga ada yang mau temenan sama lo, sendirian aja sana", "label": 1},
    {"text": "kita semua benci sama lo, pergi aja dari sini", "label": 1},
    {"text": "jangan deket-deket kita, lo nyebelin tau ga", "label": 1},
    {"text": "siapa yang mau berteman sama orang kayak lo coba", "label": 1},
    {"text": "lo ga diundang, ga perlu ikut-ikutan", "label": 1},

    # Cyberbullying / penyebaran gosip
    {"text": "gue udah sebar foto memalukan lo ke semua orang", "label": 1},
    {"text": "semua udah tau keburukan lo, malu-maluin banget", "label": 1},
    {"text": "gue screenshot chat lo terus gue sebar ya", "label": 1},
    {"text": "liat nih semua, ini orangnya yang norak banget", "label": 1},
    {"text": "gue bikin poll siapa yang paling ga berguna, lo menang", "label": 1},

    # Kata-kata kasar / makian
    {"text": "bangsat lo, nyebelin banget sih", "label": 1},
    {"text": "anjing lo tuh, ga tau diri banget", "label": 1},
    {"text": "goblok banget sih lo ini, bikin kesel aja", "label": 1},
    {"text": "brengsek lo, udah dibantu malah gitu", "label": 1},
    {"text": "sampah banget kelakuan lo", "label": 1},

    # Meremehkan / merendahkan
    {"text": "lo ga akan pernah bisa sukses, percuma aja hidup", "label": 1},
    {"text": "usaha lo itu sia-sia, dari dulu juga ga ada hasilnya", "label": 1},
    {"text": "lo tuh ga penting, ga ada lo juga ga ada bedanya", "label": 1},
    {"text": "apapun yang lo lakuin pasti gagal, udah nasib lo gitu", "label": 1},
    {"text": "mimpi aja lo bisa kayak mereka, ga mungkin", "label": 1},

    # Ejekan identitas
    {"text": "miskin kayak lo masih sok-sokan", "label": 1},
    {"text": "orang kampung emang ga tau gaya", "label": 1},
    {"text": "lo tuh norak, ketahuan ga pernah gaul", "label": 1},
    {"text": "ga heran lo ga punya teman, kepribadian lo menyebalkan", "label": 1},
    {"text": "keluarga lo aja malu punya anak kayak lo", "label": 1},

    # Ejek prestasi
    {"text": "nilai lo jelek terus, pantas aja ga naik kelas", "label": 1},
    {"text": "tim lo tuh paling lemah, gara-gara lo semua kalah", "label": 1},
    {"text": "lo tuh beban kelompok, mending ga usah ikut", "label": 1},
    {"text": "presentasi lo tadi memalukan banget, bikin kelas malu", "label": 1},
    {"text": "selalu lo yang bikin projek gagal", "label": 1},

    # ============================================================
    # NON-BULLYING (label = 0)
    # ============================================================

    # Percakapan sehari-hari
    {"text": "hei, apa kabar? sudah lama tidak ketemu", "label": 0},
    {"text": "selamat pagi, semoga harimu menyenangkan ya", "label": 0},
    {"text": "besok kita jadi pergi ke mall kan?", "label": 0},
    {"text": "tugas matematika nomor 5 susah ya, kamu udah ngerjain?", "label": 0},
    {"text": "makasih udah bantuin aku tadi, kamu baik banget", "label": 0},

    # Diskusi pelajaran
    {"text": "eh lo ngerti ga materi fisika bab 3? aku bingung banget", "label": 0},
    {"text": "belajar bareng yuk, ujian minggu depan nih", "label": 0},
    {"text": "catatan bahasa indonesia kamu boleh aku pinjam ga?", "label": 0},
    {"text": "gurunya tadi jelasinnya cepet banget, ada yang ngerti ga?", "label": 0},
    {"text": "kita bagi tugas kelompok gimana? siapa ngerjain bagian mana?", "label": 0},

    # Olahraga & kegiatan
    {"text": "besok latihan basket jam berapa? jangan telat ya", "label": 0},
    {"text": "kemarin pertandingan seru banget, tim kita main bagus", "label": 0},
    {"text": "gue mau ikut ekskul futsal, kamu mau ikut juga ga?", "label": 0},
    {"text": "jadwal renang minggu ini gimana? ada yang berubah ga?", "label": 0},
    {"text": "mantap deh, lo main bagus banget tadi di lapangan", "label": 0},

    # Pujian & dukungan
    {"text": "kamu keren banget bisa nyanyi, suaranya bagus", "label": 0},
    {"text": "gambar lo bagus banget, bakat lo di sana deh", "label": 0},
    {"text": "semangat ya, kamu pasti bisa lulus ujian itu", "label": 0},
    {"text": "lo tuh orangnya seru, enak diajak ngobrol", "label": 0},
    {"text": "kerja keras lo ga sia-sia, hasilnya kelihatan kok", "label": 0},

    # Empati & kepedulian
    {"text": "lo kenapa murung? ada masalah? cerita dong kalau mau", "label": 0},
    {"text": "tenang aja, semua orang pernah gagal, bangkit lagi ya", "label": 0},
    {"text": "aku turut sedih dengernya, semoga cepet baikan", "label": 0},
    {"text": "kalau butuh bantuan, hubungi aku aja ya jangan sungkan", "label": 0},
    {"text": "kamu udah usaha keras kok, hasilnya ga selalu instan", "label": 0},

    # Humor ringan / bercanda sehat
    {"text": "hahaha lucu banget tadi, ngakak aku dengernya", "label": 0},
    {"text": "becanda doang kali, jangan baper hehe", "label": 0},
    {"text": "wkwk iya aku juga bingung tadi, kocak banget situasinya", "label": 0},
    {"text": "lol ngapain juga gitu, tapi seru sih haha", "label": 0},
    {"text": "santai bro, gue cuma bercanda sama lo", "label": 0},

    # Rencana & koordinasi
    {"text": "meeting project jam 3 sore ya, jangan lupa", "label": 0},
    {"text": "titip absen ya kalau aku telat masuk kelas", "label": 0},
    {"text": "pulang bareng ga hari ini? searah soalnya", "label": 0},
    {"text": "ada pr apa aja buat besok? aku ketinggalan info", "label": 0},
    {"text": "makan siang di kantin yuk, laper banget nih", "label": 0},

    # Berbagi informasi
    {"text": "tadi guru bilang ujian diundur minggu depan lho", "label": 0},
    {"text": "ada event bazaar sabtu ini di sekolah, mau ikut?", "label": 0},
    {"text": "rekomendasi film bagus dong, lagi nyari tontonan nih", "label": 0},
    {"text": "ada yang tau toko buku terdekat di sini?", "label": 0},
    {"text": "info kuy, besok sekolah libur katanya", "label": 0},

    # Komentar netral / positif
    {"text": "cuaca hari ini cerah banget, enak buat olahraga", "label": 0},
    {"text": "makanan di kantin tadi enak banget, lo udah coba?", "label": 0},
    {"text": "baju baru lo bagus, cocok banget sama lo", "label": 0},
    {"text": "wah hebat, nilai lo naik terus ya belakangan ini", "label": 0},
    {"text": "program yang lo buat jalan lancar, good job", "label": 0},
]


def get_dataframe():
    """Mengembalikan dataset dalam bentuk pandas DataFrame."""
    import pandas as pd
    df = pd.DataFrame(DATASET)
    return df


def get_class_distribution(df):
    """Menampilkan distribusi kelas dalam dataset."""
    dist = df["label"].value_counts()
    print("=== Distribusi Dataset ===")
    print(f"  Non-Bullying (0): {dist.get(0, 0)} sampel")
    print(f"  Bullying     (1): {dist.get(1, 0)} sampel")
    print(f"  Total            : {len(df)} sampel")
    return dist


if __name__ == "__main__":
    df = get_dataframe()
    get_class_distribution(df)
    print("\nContoh data:")
    print(df.sample(5).to_string(index=False))
