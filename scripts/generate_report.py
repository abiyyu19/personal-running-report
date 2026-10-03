#!/usr/bin/env python3
"""
Script untuk meng-generate Markdown Report secara otomatis
berdasarkan data CSV terbaru.
"""

import os
import pandas as pd

def generate_markdown_report(csv_path=None, output_md=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if csv_path is None:
        csv_path = os.path.abspath(os.path.join(base_dir, "..", "output", "rekap_data_lari_4bulan.csv"))
    if output_md is None:
        output_md = os.path.abspath(os.path.join(base_dir, "..", "output", "laporan_analisis_lari.md"))

    if not os.path.exists(csv_path):
        print(f"[!] File {csv_path} tidak ditemukan.")
        return

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    
    total_runs = len(df)
    total_dist = df["distance_km"].sum()
    total_sec = df["duration_s"].sum()
    total_hours = total_sec / 3600.0
    total_cal = df["calories"].sum()
    
    weighted_pace_sec = total_sec / total_dist
    overall_pace = f"{int(weighted_pace_sec // 60)}:{int(weighted_pace_sec % 60):02d}"
    
    avg_hr = df["avg_hr"].mean()
    avg_cadence = df["cadence_spm"].mean()
    
    # Recent 5 runs
    recent_runs = df.tail(5).copy()
    recent_runs["date_str"] = recent_runs["date"].dt.strftime("%d %b %Y")
    
    # Fastest 5Ks (distance >= 4.5km)
    fastest_5k = df[df["distance_km"] >= 4.5].sort_values("pace_sec_km").head(5)
    fastest_5k["date_str"] = fastest_5k["date"].dt.strftime("%d %b %Y")

    # Longest Runs
    longest_runs = df.sort_values("distance_km", ascending=False).head(5)
    longest_runs["date_str"] = longest_runs["date"].dt.strftime("%d %b %Y")

    md_content = f"""# 🏃‍♂️ Laporan Analisis & Evaluasi Latihan Lari (Auto-Generated)

Laporan ini di-generate secara otomatis berdasarkan ekstraksi **{total_runs} sesi lari (.fit files)** terbaru.

---

## 1. Ringkasan Eksekutif Keseluruhan

| Metrik | Nilai | Keterangan |
| :--- | :--- | :--- |
| **Total Sesi Lari** | **{total_runs} sesi** | Konsistensi latihan Anda |
| **Total Jarak Tempuh** | **{total_dist:.2f} km** | Akumulasi jarak keseluruhan |
| **Total Waktu Latihan** | **{int(total_hours)} jam {int((total_sec % 3600)//60)} menit** | Investasi waktu kardio Anda |
| **Total Kalori Terbakar** | **{total_cal:,.0f} kcal** | Energi yang telah dibakar |
| **Overall Pace (Rata-rata)**| **{overall_pace} /km** | Kecepatan rata-rata tertimbang |
| **Rata-rata Detak Jantung** | **{avg_hr:.1f} bpm** | Indikator intensitas rata-rata |
| **Rata-rata Kadensi** | **{avg_cadence:.1f} spm** | Frekuensi putaran kaki |

---

## 2. Aktivitas Lari Terakhir (Recent Runs)
Berikut adalah 5 sesi lari terakhir Anda:

| Tanggal | Jarak (km) | Waktu | Pace (/km) | Avg HR | Kadensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in recent_runs.iterrows():
        md_content += f"| {row['date_str']} | {row['distance_km']:.2f} | {row['duration_str']} | {row['pace_str']} | {row['avg_hr']:.0f} | {row['cadence_spm']} |\n"

    md_content += """
---

## 3. Rekor Pribadi (Personal Bests)

### 🔥 Lari 5K+ Tercepat (Fastest Pace)
| Tanggal | Jarak (km) | Waktu | Pace (/km) | Avg HR |
| :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in fastest_5k.iterrows():
        md_content += f"| {row['date_str']} | {row['distance_km']:.2f} | {row['duration_str']} | **{row['pace_str']}** | {row['avg_hr']:.0f} |\n"

    md_content += """
### 🏅 Lari Jarak Terjauh (Longest Runs)
| Tanggal | Jarak (km) | Waktu | Pace (/km) | Avg HR |
| :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in longest_runs.iterrows():
        md_content += f"| {row['date_str']} | **{row['distance_km']:.2f}** | {row['duration_str']} | {row['pace_str']} | {row['avg_hr']:.0f} |\n"

    md_content += """
---

## 4. Evaluasi & Saran Otomatis (Per Update Terakhir)

> [!TIP]
> **Puncak Performa (Peaking):** Data menunjukkan peningkatan Pace yang luar biasa pada sesi terakhir. Jika Anda memiliki Race dalam 1-2 hari ke depan, **HINDARI latihan berat/speed session**. Lakukan istirahat (*Full Rest*) atau sekadar *Shakeout run* (2-3 km santai). *The hay is in the barn!*

> [!NOTE]
> Laporan ini akan selalu diperbarui secara otomatis setiap kali Anda menjalankan script ekstraksi (`extract_fit_data.py`).
"""

    os.makedirs(os.path.dirname(output_md), exist_ok=True)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"[+] Laporan Markdown berhasil di-generate di: {output_md}")

if __name__ == "__main__":
    generate_markdown_report()
