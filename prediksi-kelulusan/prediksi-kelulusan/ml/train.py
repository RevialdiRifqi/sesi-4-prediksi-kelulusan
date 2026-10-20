"""Pipeline Machine Learning sesuai tahapan materi Sesi 4."""
import json
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, mean_absolute_error)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

FITUR = ["ipk", "rata_ips_3_semester", "sks_lulus", "persen_kehadiran",
         "jumlah_mk_mengulang", "pernah_cuti", "kerja_paruh_waktu", "aktif_organisasi"]

# 1. Pengumpulan data
df = pd.read_csv("ml/data_mahasiswa.csv")

# 2. Pembersihan data (duplikat dibuang; missing value diisi median di dalam pipeline)
df = df.drop_duplicates(subset="id_anon")

# 3. Pemilihan fitur (id_anon TIDAK dipakai -> privasi & mencegah kebocoran)
X, y_cls, y_reg = df[FITUR], df["lulus_tepat_waktu"], df["lama_studi_semester"]

# 4. Pembagian data latih & uji (stratified agar proporsi kelas terjaga)
X_tr, X_te, yc_tr, yc_te, yr_tr, yr_te = train_test_split(
    X, y_cls, y_reg, test_size=0.2, random_state=42, stratify=y_cls)

# 5. Pelatihan model
clf = Pipeline([("imp", SimpleImputer(strategy="median")),
                ("rf", RandomForestClassifier(n_estimators=200, max_depth=8,
                        class_weight="balanced", random_state=42))]).fit(X_tr, yc_tr)
reg = Pipeline([("imp", SimpleImputer(strategy="median")),
                ("rf", RandomForestRegressor(n_estimators=200, max_depth=8,
                        random_state=42))]).fit(X_tr, yr_tr)

# 6. Evaluasi
pred = clf.predict(X_te)
metrik = {
    "accuracy": round(accuracy_score(yc_te, pred), 3),
    "precision": round(precision_score(yc_te, pred), 3),
    "recall": round(recall_score(yc_te, pred), 3),
    "f1_score": round(f1_score(yc_te, pred), 3),
    "mae_lama_studi_semester": round(mean_absolute_error(yr_te, reg.predict(X_te)), 3),
    "confusion_matrix": confusion_matrix(yc_te, pred).tolist(),
}
metrik["feature_importance"] = dict(sorted(
    zip(FITUR, clf.named_steps["rf"].feature_importances_.round(3).tolist()),
    key=lambda kv: -kv[1]))

print(json.dumps(metrik, indent=2))
os.makedirs("ml/model", exist_ok=True)
joblib.dump({"clf": clf, "reg": reg, "fitur": FITUR}, "ml/model/model.joblib")
json.dump(metrik, open("ml/model/metrik.json", "w"), indent=2)
