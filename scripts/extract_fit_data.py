#!/usr/bin/env python3
"""
Script untuk mengekstrak data aktivitas lari dari kumpulan file .fit
ke dalam bentuk berkas tabular (CSV) untuk analisis lanjutan.
"""

import os
import glob
import datetime
import pandas as pd
import numpy as np
from fitparse import FitFile


def extract_all_fit_files(input_dir=None, output_csv=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if input_dir is None:
        input_dir = os.path.abspath(os.path.join(base_dir, "..", "data_fit"))
    if output_csv is None:
        output_csv = os.path.abspath(os.path.join(base_dir, "..", "output", "rekap_data_lari_4bulan.csv"))

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    fit_files = sorted(glob.glob(os.path.join(input_dir, "*.fit")))

    if not fit_files:
        print(f"[!] Tidak ditemukan file .fit di folder: {input_dir}")
        return

    print(f"[*] Ditemukan {len(fit_files)} file .fit. Memulai ekstraksi...")

    rows = []
    for f in fit_files:
        fname = os.path.basename(f)
        try:
            fitfile = FitFile(f)
            session_data = {}
            for session in fitfile.get_messages("session"):
                for d in session:
                    if d.value is not None:
                        session_data[d.name] = d.value
                break

            cadences = []
            hrs = []
            speeds = []
            altitudes = []

            for r in fitfile.get_messages("record"):
                vals = {d.name: d.value for d in r if d.value is not None}
                if "cadence" in vals and vals["cadence"] > 0:
                    cadences.append(vals["cadence"])
                if "heart_rate" in vals and vals["heart_rate"] > 0:
                    hrs.append(vals["heart_rate"])
                if "enhanced_speed" in vals and vals["enhanced_speed"] > 0:
                    speeds.append(vals["enhanced_speed"])
                elif "speed" in vals and vals["speed"] > 0:
                    speeds.append(vals["speed"])
                alt = vals.get("enhanced_altitude", vals.get("altitude"))
                if alt is not None:
                    altitudes.append(alt)

            # Waktu lokal (UTC+7 / WIB)
            start_time_utc = session_data.get("start_time")
            if start_time_utc:
                start_time_local = start_time_utc + datetime.timedelta(hours=7)
            else:
                time_part = fname.split("-")[0]
                start_time_local = datetime.datetime.strptime(time_part, "%Y.%m.%d %H.%M")

            dist_m = session_data.get("total_distance", 0.0)
            dist_km = dist_m / 1000.0
            timer_s = session_data.get(
                "total_timer_time",
                session_data.get("total_moving_time", session_data.get("total_elapsed_time", 0.0)),
            )

            avg_speed_ms = session_data.get("avg_speed")
            if not avg_speed_ms and dist_m > 0 and timer_s > 0:
                avg_speed_ms = dist_m / timer_s

            pace_sec = (1000.0 / avg_speed_ms) if (avg_speed_ms and avg_speed_ms > 0) else None
            pace_str = (
                f"{int(pace_sec // 60)}:{int(pace_sec % 60):02d}" if pace_sec else "N/A"
            )

            avg_hr = session_data.get("avg_heart_rate")
            if not avg_hr and hrs:
                avg_hr = round(np.mean(hrs), 1)

            max_hr = session_data.get("max_heart_rate")
            if not max_hr and hrs:
                max_hr = max(hrs)

            avg_cadence_raw = session_data.get("avg_cadence")
            if not avg_cadence_raw and cadences:
                avg_cadence_raw = np.mean(cadences)
            max_cadence_raw = session_data.get("max_cadence")
            if not max_cadence_raw and cadences:
                max_cadence_raw = max(cadences)

            # Konversi rpm (kaki tunggal) ke spm (total kedua kaki)
            spm_avg = round(avg_cadence_raw * 2, 1) if avg_cadence_raw else None
            spm_max = round(max_cadence_raw * 2, 1) if max_cadence_raw else None

            calories = session_data.get("total_calories")

            # Estimasi akumulasi elevasi
            total_ascent = session_data.get("total_ascent")
            if total_ascent is None and len(altitudes) > 1:
                diffs = np.diff(altitudes)
                total_ascent = round(float(np.sum(diffs[diffs > 0])), 1)

            # Efisiensi Aerobik (Kecepatan m/menit dibagi Heart Rate)
            efficiency_factor = (
                round((avg_speed_ms * 60.0) / avg_hr, 3)
                if (avg_speed_ms and avg_hr and avg_hr > 0)
                else None
            )

            # Estimasi Persentase Zona Detak Jantung
            z_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            if hrs:
                for hr_val in hrs:
                    if hr_val < 130:
                        z_counts[1] += 1
                    elif hr_val <= 145:
                        z_counts[2] += 1
                    elif hr_val <= 160:
                        z_counts[3] += 1
                    elif hr_val <= 175:
                        z_counts[4] += 1
                    else:
                        z_counts[5] += 1
                tot_hr_pts = len(hrs)
                z_pct = {f"z{k}_pct": round(v / tot_hr_pts * 100, 1) for k, v in z_counts.items()}
            else:
                z_pct = {f"z{k}_pct": None for k in range(1, 6)}

            duration_formatted = (
                f"{int(timer_s // 3600):02d}:{int((timer_s % 3600) // 60):02d}:{int(timer_s % 60):02d}"
                if timer_s >= 3600
                else f"{int(timer_s // 60):02d}:{int(timer_s % 60):02d}"
            )

            row = {
                "filename": fname,
                "date": start_time_local.strftime("%Y-%m-%d"),
                "time": start_time_local.strftime("%H:%M"),
                "day_of_week": start_time_local.strftime("%A"),
                "month": start_time_local.strftime("%Y-%m"),
                "distance_km": round(dist_km, 2),
                "duration_s": timer_s,
                "duration_min": round(timer_s / 60.0, 1),
                "duration_str": duration_formatted,
                "pace_sec_km": round(pace_sec, 1) if pace_sec else None,
                "pace_str": pace_str,
                "speed_kmh": round(avg_speed_ms * 3.6, 2) if avg_speed_ms else None,
                "avg_hr": int(round(avg_hr)) if avg_hr else None,
                "max_hr": int(round(max_hr)) if max_hr else None,
                "cadence_spm": spm_avg,
                "max_cadence_spm": spm_max,
                "calories": calories,
                "total_ascent_m": total_ascent,
                "efficiency_factor": efficiency_factor,
                **z_pct,
            }
            rows.append(row)
        except Exception as e:
            print(f"[!] Gagal membaca {fname}: {e}")

    df = pd.DataFrame(rows)
    df.sort_values("date", inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"[+] Berhasil mengekstrak {len(df)} sesi lari ke: {output_csv}")


from generate_report import generate_markdown_report

if __name__ == "__main__":
    extract_all_fit_files()
    print("[*] Menjalankan pembaruan laporan otomatis...")
    generate_markdown_report()
