# 🏃‍♂️ Personal Running Tracker & Data Pipeline

Selamat datang di repositori pelacakan dan analisis lari pribadi saya! Repositori ini tidak hanya menyimpan rekam jejak lari harian, tetapi juga difungsikan sebagai sebuah *data pipeline* otomatis yang mengubah file mentah olahraga (format `.fit`) menjadi analisis statistik dan laporan performa (Markdown & CSV) secara instan.

## 🌟 Fitur Utama
* **Ekstraksi Otomatis:** Mengurai data biner `.fit` (dari jam tangan olahraga) menjadi data metrik yang rapi (Jarak, *Pace*, *Heart Rate*, Kadensi).
* **Auto-Generated Report:** Setiap penambahan data akan secara otomatis membangun ulang dan meng-*update* statistik performa di [laporan_analisis_lari.md](output/laporan_analisis_lari.md).
* **Smart GitHub Sync:** Pembaruan data otomatis diunggah ke GitHub dengan pesan *commit* yang cerdas dan informatif (contoh: `🏃 2026-10-03: 3.41km (Pace 7:31) | Sesi ke-52`).

---

## 📂 Struktur Direktori

```text
Running Data/
├── data_fit/                         # [Data Mentah] Kumpulan file aktivitas .fit
├── output/                           # [Hasil Analisis]
│   ├── rekap_data_lari_4bulan.csv    # Master data tabular (seluruh riwayat lari)
│   └── laporan_analisis_lari.md      # Auto-generated Laporan Performa (Wajib Baca!)
├── scripts/                          # [Source Code] Pipeline Python
│   ├── extract_fit_data.py           # Ekstraktor .fit ke CSV & pemanggil generator
│   ├── generate_report.py            # Pembuat laporan Markdown otomatis
│   ├── analyze_running_data.py       # Penganalisis statistik CLI di terminal
│   └── sync_github.py                # Skrip sinkronisasi pintar ke GitHub
└── README.md                         # Dokumentasi repositori ini
```

---

## 🚀 Panduan Penggunaan (*Workflow*)

*Pipeline* di repositori ini dirancang agar sangat minim sentuhan (*frictionless*) setelah sesi lari.

### 1. Persiapan Awal
Pastikan Anda sudah menginstal pustaka yang dibutuhkan:
```bash
pip install -r scripts/requirements.txt
```

### 2. Memasukkan Data Baru
Setiap selesai berlari, letakkan file `.fit` terbaru ke dalam folder `data_fit/`.

### 3. Ekstraksi & Update Laporan (1-Click)
Jalankan skrip ini untuk mengekstrak data `.fit` baru. Skrip ini juga akan langsung memicu pembuatan ulang laporan Markdown Anda secara otomatis:
```bash
python3 scripts/extract_fit_data.py
```

### 4. Sinkronisasi Otomatis ke GitHub
Untuk melakukan *backup* ke repositori publik ini dengan pesan *commit* yang mencatat jarak dan *pace* Anda secara otomatis, cukup jalankan:
```bash
python3 scripts/sync_github.py
```

---

## 🎯 Target Race 

Repositori ini juga digunakan untuk mengawal program latihan menuju *race* yang telah ditargetkan:

1. **PLN Mobile Electric 5K Series (Selesai ✅)**
   * **Tanggal:** Minggu, 27 September 2026
   * **Lokasi:** Taman Mini Indonesia Indah (TMII), Jakarta
   * **Hasil:** Memecahkan PB (*Personal Best*) 5K dalam **31:48** (Pace 6:20/km)!

2. **KAI Commuter Run 2026 ⏳**
   * **Tanggal:** Minggu, 4 Oktober 2026
   * **Lokasi:** Stasiun BNI City, Sudirman, Jakarta Pusat
   * **Kategori:** 5K
   * **Karakteristik:** Rute aspal sangat datar dan steril (*fast course*), panggung yang sempurna untuk mengejar rekor PB baru.

---
*Ditenagai oleh Python, Data Science, dan Konsistensi.* 💪
