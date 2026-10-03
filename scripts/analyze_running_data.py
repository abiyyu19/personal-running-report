#!/usr/bin/env python3
"""
Script analisis statistik dan tren performa latihan lari dari file rekap CSV.
"""

import os
import pandas as pd
import numpy as np


def analyze_data(csv_path=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if csv_path is None:
        csv_path = os.path.abspath(os.path.join(base_dir, "..", "output", "rekap_data_lari_4bulan.csv"))

    if not os.path.exists(csv_path):
        print(f"[!] File data tidak ditemukan: {csv_path}")
        print("Silakan jalankan extract_fit_data.py terlebih dahulu.")
        return

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.to_period("W").astype(str)

    print("=" * 60)
    print("           RINGKASAN TOTAL LATIHAN LARI 4 BULAN")
    print("=" * 60)
    total_runs = len(df)
    total_dist = df["distance_km"].sum()
    total_sec = df["duration_s"].sum()
    total_hours = total_sec / 3600.0
    total_cal = df["calories"].sum()
    avg_dist = df["distance_km"].mean()
    avg_dur = df["duration_min"].mean()
    weighted_pace_sec = total_sec / total_dist
    w_min = int(weighted_pace_sec // 60)
    w_sec = int(weighted_pace_sec % 60)

    print(f"Total Sesi Lari        : {total_runs} sesi")
    print(f"Total Jarak Tempuh     : {total_dist:.2f} km")
    print(f"Total Waktu Latihan    : {int(total_hours)} jam {int((total_sec % 3600) // 60)} menit ({total_hours:.1f} jam)")
    print(f"Total Kalori Terbakar  : {total_cal:,.0f} kcal")
    print(f"Rata-rata Jarak/Sesi   : {avg_dist:.2f} km")
    print(f"Rata-rata Durasi/Sesi  : {avg_dur:.1f} menit")
    print(f"Pace Rata-rata Total   : {w_min}:{w_sec:02d} /km")
    print(f"Rerata Detak Jantung   : {df['avg_hr'].mean():.1f} bpm (Max: {df['max_hr'].max()} bpm)")
    print(f"Rerata Kadensi (SPM)   : {df['cadence_spm'].mean():.1f} spm (Max: {df['max_cadence_spm'].max():.1f} spm)")
    print(f"Efficiency Factor (EF) : {df['efficiency_factor'].mean():.3f}")

    print("\n" + "=" * 60)
    print("                   PROGRES BULANAN")
    print("=" * 60)
    monthly = df.groupby("month").agg(
        sesi=("distance_km", "count"),
        total_km=("distance_km", "sum"),
        rerata_km=("distance_km", "mean"),
        max_km=("distance_km", "max"),
        rerata_pace_sec=("pace_sec_km", "mean"),
        rerata_hr=("avg_hr", "mean"),
        rerata_spm=("cadence_spm", "mean"),
        efisiensi=("efficiency_factor", "mean")
    ).reset_index()

    monthly["pace"] = monthly["rerata_pace_sec"].apply(lambda s: f"{int(s//60)}:{int(s%60):02d}")
    display_monthly = monthly[["month", "sesi", "total_km", "rerata_km", "max_km", "pace", "rerata_hr", "rerata_spm", "efisiensi"]].copy()
    display_monthly["total_km"] = display_monthly["total_km"].round(2)
    display_monthly["rerata_km"] = display_monthly["rerata_km"].round(2)
    display_monthly["rerata_hr"] = display_monthly["rerata_hr"].round(1)
    display_monthly["rerata_spm"] = display_monthly["rerata_spm"].round(1)
    display_monthly["efisiensi"] = display_monthly["efisiensi"].round(3)
    print(display_monthly.to_string(index=False))

    print("\n" + "=" * 60)
    print("             TOP 5 LARI TERJAUH (LONG RUNS)")
    print("=" * 60)
    longest = df.sort_values("distance_km", ascending=False).head(5)
    print(longest[["date", "distance_km", "duration_str", "pace_str", "avg_hr", "cadence_spm"]].to_string(index=False))

    print("\n" + "=" * 60)
    print("             TOP 5 LARI TERCEPAT (JARAK >= 4 KM)")
    print("=" * 60)
    fastest = df[df["distance_km"] >= 4.0].sort_values("pace_sec_km", ascending=True).head(5)
    print(fastest[["date", "distance_km", "duration_str", "pace_str", "avg_hr", "cadence_spm"]].to_string(index=False))
    print("=" * 60)


if __name__ == "__main__":
    analyze_data()
