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

    # Lihat file apa saja yang berubah
    staged = subprocess.run(["git", "diff", "--name-only", "--cached"], cwd=repo_dir, capture_output=True, text=True)
    staged_files = staged.stdout.strip().split("\n")

    has_data = any(f.endswith('.fit') or 'rekap_data_lari' in f for f in staged_files)
    has_script = any('scripts/' in f for f in staged_files)
    has_readme = any('README.md' in f for f in staged_files)

    # Buat pesan commit otomatis yang cerdas sesuai konteks
    commit_msg = f"🔄 Update repositori pada {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    if has_data and os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if not df.empty:
                latest = df.iloc[-1]
                date_str = latest['date']
                dist = latest['distance_km']
                pace = latest['pace_str']
                total_runs = len(df)
                commit_msg = f"🏃 {date_str}: {dist:.2f}km (Pace {pace}) | Sesi ke-{total_runs}"
        except Exception as e:
            pass
    elif has_readme and not has_script:
        commit_msg = "📝 Update dokumentasi README.md"
    elif has_script and not has_readme:
        commit_msg = "🔧 Update skrip otomatisasi Python"
    elif has_readme and has_script:
        commit_msg = "⚙️ Update dokumentasi dan skrip otomatisasi"

    print("\n=========================================")
    print("[?] RENCANA COMMIT & PUSH")
    print("=========================================")
    print(f"Pesan Commit : {commit_msg}")
    print("File Berubah :")
    for f in staged_files:
        print(f"  - {f}")
    print("=========================================\n")

    # Meminta persetujuan pengguna
    import sys
    # Memeriksa jika script dijalankan secara non-interaktif (misal oleh AI)
    if not sys.stdin.isatty():
        print("[!] Mode non-interaktif terdeteksi. Dibatalkan agar menunggu review manual.")
        return

    ans = input("Apakah Anda menyetujui rencana di atas? (y/n/edit): ").strip().lower()
    if ans == 'n':
        print("[-] Operasi dibatalkan.")
        return
    elif ans == 'edit':
        custom_msg = input("Masukkan pesan commit kustom: ").strip()
        if custom_msg:
            commit_msg = custom_msg

    print(f"\n[*] Melakukan commit dengan pesan: '{commit_msg}'")
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir)
    
    print("[*] Mengunggah (pushing) data ke GitHub...")
    push_result = subprocess.run(["git", "push"], cwd=repo_dir)
    
    if push_result.returncode == 0:
        print("[+] Sinkronisasi ke GitHub berhasil diselesaikan! 🚀")
    else:
        print("[-] Gagal melakukan git push. Pastikan koneksi internet aman.")

if __name__ == "__main__":
    sync_to_github()
