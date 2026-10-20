"""API prediksi (Flask), dipanggil oleh Laravel lewat HTTP.
Jalankan: python ml/api.py  -> http://127.0.0.1:5000"""
import os
import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)
M = joblib.load(os.path.join(os.path.dirname(__file__), "model", "model.joblib"))
BATAS = {"ipk": (0, 4), "rata_ips_3_semester": (0, 4), "sks_lulus": (0, 160),
         "persen_kehadiran": (0, 100), "jumlah_mk_mengulang": (0, 30)}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    # Validasi input: data baru bisa saja di luar kewajaran
    for f in M["fitur"]:
        if f not in data:
            return jsonify(error=f"Field '{f}' wajib diisi"), 422
        if f in BATAS and not (BATAS[f][0] <= float(data[f]) <= BATAS[f][1]):
            return jsonify(error=f"Nilai '{f}' di luar rentang {BATAS[f]}"), 422
    X = pd.DataFrame([{f: float(data[f]) for f in M["fitur"]}])
    p = float(M["clf"].predict_proba(X)[0][1])
    sem = float(M["reg"].predict(X)[0])
    risiko = "RENDAH" if p >= 0.75 else "SEDANG" if p >= 0.5 else "TINGGI"
    return jsonify(peluang_tepat_waktu=round(p, 3), risiko=risiko,
                   estimasi_lama_studi_semester=round(sem, 1))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
