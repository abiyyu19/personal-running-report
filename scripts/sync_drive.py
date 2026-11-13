#!/usr/bin/env python3
"""
Script untuk menyinkronkan (download) file aktivitas lari terbaru (.fit)
secara otomatis dari Google Drive (folder 'Health Sync Activities')
ke direktori lokal 'data_fit/', lalu otomatis memperbarui laporan.
"""

import os
import glob
import json
import subprocess
import sys

DRIVE_FOLDER_ID = "164POmJY25F4YxHCb7JuXLXybDCDPT3pe"  # Health Sync Activities

def sync_from_drive():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_fit_dir = os.path.abspath(os.path.join(base_dir, "..", "data_fit"))
    os.makedirs(data_fit_dir, exist_ok=True)

    print("[*] Memeriksa file aktivitas lari di Google Drive (Health Sync Activities)...")
    
    cmd = [
        "gdrive", "readonly", "search",
        "--parent-id", DRIVE_FOLDER_ID,
        "--name-contains", "RUNNING.fit",
        "--json"
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Gagal menghubungi Google Drive: {res.stderr}")
        return False

    try:
        remote_items = json.loads(res.stdout)
    except Exception as e:
        print(f"[!] Gagal membaca response JSON dari gdrive: {e}")
        return False

    local_existing = set(os.path.basename(f) for f in glob.glob(os.path.join(data_fit_dir, "*.fit")))
    
    new_downloads = []
    for item in remote_items:
        fname = item.get("name")
        fid = item.get("id")
        if fname and fname.endswith(".fit") and fname not in local_existing:
            new_downloads.append((fname, fid))

    if not new_downloads:
        print(f"[✓] Semua data lari sudah up-to-date! Tidak ada file baru yang perlu diunduh ({len(local_existing)} file lokal).")
        return False

    print(f"[*] Ditemukan {len(new_downloads)} aktivitas baru di Google Drive:")
    for fname, _ in new_downloads:
        print(f"    - {fname}")

    downloaded_count = 0
    for fname, fid in new_downloads:
        dest_path = os.path.join(data_fit_dir, fname)
        dl_cmd = ["gdrive", "readonly", "download", fid, "--out", dest_path]
        print(f"[*] Mengunduh {fname}...", end=" ", flush=True)
        dl_res = subprocess.run(dl_cmd, capture_output=True, text=True)
        if dl_res.returncode == 0 and os.path.exists(dest_path):
            print("Done ✓")
            downloaded_count += 1
        else:
            print(f"Gagal ✗ ({dl_res.stderr.strip()})")

    print(f"\n[+] Berhasil mengunduh {downloaded_count} file baru ke folder data_fit/.")
    return downloaded_count > 0

if __name__ == "__main__":
    has_new = sync_from_drive()
    if has_new:
        print("\n[*] Menjalankan pipeline ekstraksi data dan generate laporan...")
        from extract_fit_data import extract_all_fit_files
        from generate_report import generate_markdown_report
        extract_all_fit_files()
        generate_markdown_report()
        print("[✓] Pipeline sinkronisasi selesai sempurna!")
