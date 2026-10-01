# studio-gpu-watchdog

Penjaga **di luar VPS** untuk pod GPU Runpod milik `studio-video-ai`.

Pod GPU tidak memegang kunci Runpod (keputusan pemilik 2026-10-01) — yang menghapus pod adalah
autoscaler di VPS. Kalau VPS atau autoscaler mati lama, tidak ada yang menghentikan tagihan.
Workflow di repo ini jalan di runner GitHub tiap 10 menit:

1. `GET https://app.sekalibanyak.com/api/healthz/autoscaler` — 200 hanya bila aplikasi hidup
   **dan** heartbeat autoscaler masih segar.
2. Bila bukan 200: tunggu `OUTAGE_MINUTES` (bawaan 15), cek lagi. Masih bukan 200 → hapus semua pod
   Runpod yang namanya berawalan `POD_NAME_PREFIX` (bawaan `studio-worker-`) dan buka *issue* di repo
   ini (pemilik dapat e-mail).
3. Tidak pernah membuat pod. Tidak menyentuh pod lain.

Batas kerugian saat VPS mati total: ±15–35 menit tagihan (jeda cron + jendela tunggu), bukan "sampai
saldo habis".

## Pengaturan (Settings repo)
- **Secret** `RUNPOD_API_KEY` — kunci akun Runpod (terenkripsi oleh GitHub; tidak pernah tampil di log).
- **Variables**: `APP_URL`, `POD_NAME_PREFIX`, `OUTAGE_MINUTES`, `WATCHDOG_ENABLED` (`false` untuk mematikan).

## Pemicu
Jadwal bawaan GitHub (`schedule`, tiap 10 menit) **di akun ini telat berjam-jam / belum pernah jalan**,
jadi watchdog ini hanya **pengaman tambahan**, bukan jaminan. Pemilik memutuskan (2026-10-02) **tidak**
memakai layanan luar (cron-job.org, healthchecks.io). Pengaman utama ada di aplikasi sendiri — lihat
`docs/RISIKO.md` bagian "Rencana final" di repo `studio-video-ai`.
Workflow sengaja **tanpa input**: run apa pun hanya bisa *memeriksa*.
Rencana (PR-2): bertindak hanya bila `/api/readyz` gagal 2× berjarak 15 menit — bukan karena heartbeat
autoscaler basi (yang sekarang bisa menghapus pod yang sedang kerja).

## Tombol darurat
Hapus pod langsung di **console Runpod → Pods → Terminate** (atau tombol darurat di aplikasi).

Repo ini publik hanya berisi workflow (tanpa rahasia) karena Actions gratis untuk repo publik.

_Terakhir diperiksa: 2026-10-01._
