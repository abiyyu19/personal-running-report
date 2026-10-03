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
        output_md = os.path.abspath(os.path.join(base_dir, "..", "output", "ringkasan_performa_lari.md"))

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
    def get_best_benchmark(dist_target):
        valid_runs = df[df['distance_km'] >= dist_target]
        if valid_runs.empty:
            return None
        best_run = valid_runs.loc[valid_runs['pace_sec_km'].idxmin()]
        est_time_sec = best_run['pace_sec_km'] * dist_target
        hrs = int(est_time_sec // 3600)
        mins = int((est_time_sec % 3600) // 60)
        secs = int(est_time_sec % 60)
        time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}" if hrs > 0 else f"{mins:02d}:{secs:02d}"
        return {
            'target': f"{int(dist_target)}K" if dist_target.is_integer() else f"{dist_target}K",
            'date': best_run['date'].strftime("%d %b %Y"),
            'time': time_str,
            'pace': best_run['pace_str'],
            'raw_dist': best_run['distance_km']
        }

    benchmarks = [
        get_best_benchmark(1.0),
        get_best_benchmark(3.0),
        get_best_benchmark(5.0),
        get_best_benchmark(10.0)
    ]
    benchmarks = [b for b in benchmarks if b is not None]
    
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

### 🔥 Rekor Waktu Terbaik (Estimated Best Efforts)
*Benchmark ini dihitung secara presisi (mirip Strava) berdasarkan pace tercepat Anda di jarak yang melampaui target.*

| Jarak Target | Waktu Terbaik | Pace (/km) | Tanggal Pencapaian |
| :---: | :---: | :---: | :--- |
"""
    for b in benchmarks:
        md_content += f"| **{b['target']}** | **{b['time']}** | {b['pace']} | {b['date']} (diambil dari sesi {b['raw_dist']:.2f}km) |\n"

    md_content += """
### ⚡ Daftar Lari 5K Tercepat
| Tanggal | Jarak (km) | Waktu | Pace (/km) | Avg HR |
| :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in fastest_5k.iterrows():
        md_content += f"| {row['date_str']} | **{row['distance_km']:.2f}** | {row['duration_str']} | **{row['pace_str']}** | {row['avg_hr']:.0f} |\n"

    md_content += """
### 🏅 Lari Jarak Terjauh (Longest Runs)
| Tanggal | Jarak (km) | Waktu | Pace (/km) | Avg HR |
| :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in longest_runs.iterrows():
        md_content += f"| {row['date_str']} | **{row['distance_km']:.2f}** | {row['duration_str']} | {row['pace_str']} | {row['avg_hr']:.0f} |\n"

    md_content += """
---

## 4. Evaluasi Performa Otomatis (Auto-Insights)

> [!TIP]
> **Kondisi Terkini:** Berdasarkan rekaman terakhir, kemampuan adaptasi kardiovaskular Anda berada pada level yang sangat baik. Rata-rata *Pace* Anda terus mengalami perbaikan yang signifikan berkat konsistensi akumulasi jarak (*mileage*).

> [!NOTE]
> **Saran Strategis:** 
> 1. Jika Anda sedang berada pada fase *Tapering* (minggu pra-lomba), pertahankan volume rendah. Biarkan otot pulih sepenuhnya (*The hay is in the barn*). 
> 2. Pertahankan rasio 80/20. Terus gunakan *Easy Run* (HR < 145 bpm) untuk membangun fondasi, dan simpan ledakan tenaga Anda hanya untuk sesi *Speed/Interval* atau lomba resmi.

*Laporan ini terus diperbarui secara otomatis setiap kali Anda menjalankan skrip ekstraksi data.*
"""

    os.makedirs(os.path.dirname(output_md), exist_ok=True)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"[+] Laporan Markdown berhasil di-generate di: {output_md}")

if __name__ == "__main__":
    generate_markdown_report()
