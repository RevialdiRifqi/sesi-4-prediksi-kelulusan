"""Membuat dataset SINTETIS (bukan data mahasiswa asli) untuk simulasi.
Alasan: privasi data -- data akademik asli bersifat sensitif.
Sengaja ditambah missing value agar tahap 'pembersihan data' bermakna."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 1500

ipk = np.clip(rng.normal(3.1, 0.45, N), 1.5, 4.0)
rata_ips_3 = np.clip(ipk + rng.normal(0, 0.25, N), 1.0, 4.0)
sks_lulus = np.clip((ipk - 1.5) * 12 + rng.normal(100, 18, N), 40, 144).round()
hadir = np.clip(rng.normal(85, 10, N) + (ipk - 3) * 5, 40, 100)
mengulang = np.clip(rng.poisson(np.clip(4 - ipk, 0.1, 3), N), 0, 10)
cuti = rng.binomial(1, 0.08, N)
kerja = rng.binomial(1, 0.22, N)
organisasi = rng.binomial(1, 0.35, N)

skor = (2.2 * (ipk - 3.0) + 1.2 * (rata_ips_3 - 3.0) + 0.04 * (sks_lulus - 100)
        + 0.04 * (hadir - 80) - 0.6 * mengulang - 1.8 * cuti - 0.5 * kerja
        + 0.1 * organisasi + 0.8 + rng.normal(0, 0.8, N))
tepat = (1 / (1 + np.exp(-skor)) > 0.5).astype(int)
lama = np.where(tepat == 1, 8, 9 + np.clip(mengulang // 2 + cuti * 2 + rng.integers(0, 3, N), 0, 6))

df = pd.DataFrame({
    "id_anon": [f"M{i:05d}" for i in range(N)], "ipk": ipk.round(2),
    "rata_ips_3_semester": rata_ips_3.round(2), "sks_lulus": sks_lulus,
    "persen_kehadiran": hadir.round(1), "jumlah_mk_mengulang": mengulang,
    "pernah_cuti": cuti, "kerja_paruh_waktu": kerja, "aktif_organisasi": organisasi,
    "lama_studi_semester": lama, "lulus_tepat_waktu": tepat,
})
for col in ["persen_kehadiran", "rata_ips_3_semester"]:  # data kotor
    df.loc[rng.choice(N, 40, replace=False), col] = np.nan
df.to_csv("ml/data_mahasiswa.csv", index=False)
print("Dataset dibuat:", df.shape, "| proporsi tepat waktu:", round(tepat.mean(), 2))
