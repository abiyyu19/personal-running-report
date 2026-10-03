#!/usr/bin/env python3
import os
import subprocess
import pandas as pd
from datetime import datetime

def sync_to_github():
    # Tentukan path utama
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.abspath(os.path.join(base_dir, ".."))
    csv_path = os.path.join(repo_dir, "output", "rekap_data_lari_4bulan.csv")
    
    print("[*] Menambahkan file ke Git (git add .)...")
    subprocess.run(["git", "add", "."], cwd=repo_dir)
    
    # Cek apakah ada perubahan yang perlu di-commit
    status = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
    if not status.stdout.strip():
        print("[!] Tidak ada file baru atau perubahan untuk di-commit.")
        return

    # Buat pesan commit otomatis yang cerdas
    commit_msg = f"Update repositori pada {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if not df.empty:
                latest = df.iloc[-1]
                date_str = latest['date']
                dist = latest['distance_km']
                pace = latest['pace_str']
                total_runs = len(df)
                
                # Format: "🏃 2026-10-03: 3.41km (Pace 7:31) | Sesi ke-52"
                commit_msg = f"🏃 {date_str}: {dist:.2f}km (Pace {pace}) | Sesi ke-{total_runs}"
        except Exception as e:
            print(f"[!] Gagal membaca CSV untuk pesan commit: {e}")

    print(f"[*] Melakukan commit dengan pesan: '{commit_msg}'")
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir)
    
    print("[*] Mengunggah (pushing) data ke GitHub...")
    push_result = subprocess.run(["git", "push"], cwd=repo_dir)
    
    if push_result.returncode == 0:
        print("[+] Sinkronisasi ke GitHub berhasil diselesaikan! 🚀")
    else:
        print("[-] Gagal melakukan git push. Pastikan koneksi internet aman.")

if __name__ == "__main__":
    sync_to_github()
