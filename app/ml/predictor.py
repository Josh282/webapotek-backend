import os
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import datetime, timedelta
from crud.pemakaian import get_all_pemakaian

MODEL_PATH = os.path.join(os.path.dirname(__file__), "xgb_model_stok_obat.json")

try:
    booster = xgb.Booster()
    booster.load_model(MODEL_PATH)
except Exception as e:
    print("❌ Gagal load model XGBoost:", e)
    booster = None

def predict_from_pemakaian(db, horizon=1):
    if booster is None:
        raise RuntimeError("Model belum berhasil diload.")

    records = get_all_pemakaian(db)
    if not records:
        return []

    df = pd.DataFrame([{
        "namaobat": r.namaobat,
        "jumlah": r.jumlah,
        "bulan": r.bulan
    } for r in records])

    df_feat = df.groupby("namaobat")["jumlah"].sum().reset_index()
    df_feat["total_volume"] = df_feat["jumlah"]
    df_feat["avg_3bulan"] = df_feat["jumlah"] / 3
    df_feat["flag_lonjakan"] = df_feat["jumlah"].apply(lambda x: 1 if x > 100 else 0)

    now = datetime.today()
    bulan_prediksi = (now.month + horizon - 1) % 12 + 1
    tahun_prediksi = now.year + ((now.month + horizon - 1) // 12)

    df_feat["bulan_num"] = bulan_prediksi
    df_feat["tahun"] = tahun_prediksi

    X = df_feat[["total_volume", "avg_3bulan", "bulan_num", "tahun", "flag_lonjakan"]]
    dmatrix = xgb.DMatrix(X.values, feature_names=X.columns)

    preds = booster.predict(dmatrix)

    output = []
    for i, row in df_feat.iterrows():
        output.append({
            "obat": row["namaobat"],
            "bulan": f"{int(row['tahun'])}-{str(int(row['bulan_num'])).zfill(2)}",
            "jumlah": int(preds[i])
        })

    return output
