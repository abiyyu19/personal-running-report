# Running Data Workspace

Struktur folder workspace pelacakan dan analisis latihan lari:

```text
Running Data/
├── data_fit/                         # Direktori file mentah aktivitas lari (.fit)
│   ├── 2026.06.05 16.58-RUNNING.fit
│   └── ... (total 49 file)
├── output/                           # Hasil ekstraksi data dan laporan analisis
│   ├── rekap_data_lari_4bulan.csv    # Rekap data tabular seluruh sesi
│   └── laporan_analisis_4bulan.md    # Dokumen analisis lengkap & evaluasi
├── scripts/                          # Kode Python untuk pengolahan data
│   ├── extract_fit_data.py           # Script ekstraksi dari .fit ke CSV
│   ├── analyze_running_data.py       # Script analisis statistik & metrik
│   └── requirements.txt              # Daftar pustaka Python yang dibutuhkan
└── README.md                         # Panduan folder ini
```

---

## Cara Menjalankan Script

### 1. Instalasi Pustaka
```bash
pip install -r scripts/requirements.txt
```

### 2. Ekstraksi File FIT ke CSV
Jika Anda menambahkan file `.fit` baru ke dalam folder `data_fit/`, jalankan:
```bash
python3 scripts/extract_fit_data.py
```
Hasil pembaruan akan otomatis tersimpan di `output/rekap_data_lari_4bulan.csv` dan laporan Markdown terbaru akan di-generate secara otomatis di `output/laporan_analisis_lari.md`.

### 3. Menampilkan Analisis & Statistik
Untuk melihat ringkasan perkembangan mingguan, bulanan, dan rekor lari di terminal:
```bash
python3 scripts/analyze_running_data.py
```

---

## 🏃‍♂️ Upcoming Races (Event Mendatang)

Workspace ini juga digunakan untuk memantau persiapan menuju dua race target terdekat:

1. **PLN Mobile Electric 5K Series**
   * **Tanggal:** Minggu, 27 September 2026
   * **Lokasi:** Taman Mini Indonesia Indah (TMII), Jakarta
   * **Kategori:** 5K
   * **Karakteristik:** Rute bergelombang ringan (*rolling hills*), start pagi.

2. **KAI Commuter Run 2026**
   * **Tanggal:** Minggu, 4 Oktober 2026
   * **Lokasi:** Stasiun BNI City, Sudirman, Jakarta Pusat
   * **Kategori:** 5K
   * **Karakteristik:** Rute aspal sangat datar dan steril (*fast course*), ideal untuk target *Personal Best* (PB).
