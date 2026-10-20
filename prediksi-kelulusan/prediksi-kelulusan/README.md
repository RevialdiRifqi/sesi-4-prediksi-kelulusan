# Sistem Prediksi Kelulusan Mahasiswa Tepat Waktu (Random Forest, Laravel + Python)

Studi kasus penerapan materi **Sesi 4: Machine Learning**.

## 1. Latar Belakang
Keterlambatan studi merugikan mahasiswa (biaya, waktu) dan institusi (akreditasi). Jika risiko dapat dikenali sejak dini
dari data akademik, dosen wali dapat memberi pendampingan lebih awal.

**Rumusan masalah:** bagaimana memprediksi peluang mahasiswa lulus tepat waktu (8 semester) dari data akademiknya?

## 2. Keterkaitan dengan Materi Pemateri
| Materi Sesi 4 | Penerapan di proyek |
|---|---|
| Supervised Learning (data berlabel) | Label `lulus_tepat_waktu` (0/1) dan `lama_studi_semester` |
| Pengumpulan data | `ml/generate_data.py` menghasilkan dataset sintetis 1.500 mahasiswa |
| Pembersihan data | Hapus duplikat, isi missing value dengan median (`SimpleImputer`) |
| Pemilihan fitur | 8 fitur akademik/non-akademik; `id_anon` sengaja tidak dipakai |
| Pembagian data latih/uji | 80/20, *stratified* |
| Pelatihan model | `RandomForestClassifier` (klasifikasi) dan `RandomForestRegressor` (estimasi semester) |
| Evaluasi: accuracy, precision, recall, F1 | Klasifikasi, lihat `ml/model/metrik.json` |
| Evaluasi: MAE | Regresi lama studi |
| Kualitas data | Data kotor disimulasikan (missing value) lalu ditangani |
| Bias data | Fitur sensitif (gender, suku, agama, penghasilan orang tua) tidak digunakan |
| Privasi | Data sintetis, ID dianonimkan, hasil prediksi tidak disimpan di DB |
| Data baru | Validasi rentang input di Laravel dan Python |
| Kebutuhan komputasi | Random Forest ringan, cukup CPU biasa |

## 3. Arsitektur
```
Browser --> Laravel (form, validasi, tampilan) --HTTP/JSON--> Flask API (Python) --> model.joblib (Random Forest)
```

## 4. Hasil Evaluasi (data uji 300 sampel, dataset sintetis)
| Metrik | Nilai |
|---|---|
| Accuracy | 0.870 |
| Precision | 0.911 |
| Recall | 0.898 |
| F1-score | 0.905 |
| MAE lama studi | 0.54 semester |

Fitur paling berpengaruh: IPK (0.31), rata-rata IPS 3 semester (0.25), SKS lulus (0.16), MK mengulang (0.13).

> Catatan: hasil di atas berasal dari data **sintetis** sehingga hanya menunjukkan alur kerja. Untuk penelitian
> sebenarnya, ganti `ml/data_mahasiswa.csv` dengan data asli (dengan izin dan anonimisasi), lalu latih ulang.

## 5. Cara Menjalankan
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python ml/generate_data.py      # buat dataset
python ml/train.py              # latih & evaluasi, model tersimpan di ml/model/
python ml/api.py                # API di http://127.0.0.1:5000
```
Contoh uji API:
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" \
 -d '{"ipk":3.6,"rata_ips_3_semester":3.5,"sks_lulus":110,"persen_kehadiran":92,"jumlah_mk_mengulang":0,"pernah_cuti":0,"kerja_paruh_waktu":0,"aktif_organisasi":1}'
```
Lalu pasang sisi web dengan mengikuti `laravel/README-INTEGRASI.md`.

## 6. Keterbatasan & Pengembangan
- Model tidak boleh menjadi satu-satunya dasar keputusan; gunakan sebagai alat bantu dosen wali.
- Perbandingan dengan algoritma lain (Logistic Regression, XGBoost) dan *cross-validation*.
- Autentikasi (dosen wali/admin), dashboard, dan penjelasan prediksi (SHAP).
