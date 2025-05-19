import os
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import datetime
from app.crud.pemakaian import get_all_pemakaian

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

    # Buat DataFrame dari hasil pemakaian
    df = pd.DataFrame([{
        "namaobat": r.namaobat,
        "jumlah": r.jumlah,
        "bulan": r.bulan
    } for r in records])

    # Ubah ke datetime
    df["bulan"] = pd.to_datetime(df["bulan"])
    now = datetime.today().replace(day=1)

    all_forecasts = []

    for obat, df_obat in df.groupby("namaobat"):
        df_obat = df_obat.sort_values("bulan").reset_index(drop=True)

        # Ambil 3 bulan terakhir (atau padding jika < 3)
        last_3 = df_obat.tail(3)["jumlah"].tolist()
        if len(last_3) < 3:
            last_3 = [0] * (3 - len(last_3)) + last_3

        total_volume = sum(last_3)
        avg_3bulan = total_volume / 3
        flag_lonjakan = 1 if total_volume > 100 else 0

        for h in range(1, horizon + 1):
            pred_month = now + pd.DateOffset(months=h)
            bulan_num = pred_month.month
            tahun = pred_month.year

            # Buat fitur untuk bulan ke-h
            feat = pd.DataFrame([{
                "total_volume": total_volume,
                "avg_3bulan": avg_3bulan,
                "bulan_num": bulan_num,
                "tahun": tahun,
                "flag_lonjakan": flag_lonjakan
            }])

            dmatrix = xgb.DMatrix(feat.values, feature_names=feat.columns)
            pred = booster.predict(dmatrix)[0]

            if h == horizon:
                all_forecasts.append({
                    "obat": obat,
                    "bulan": f"{tahun}-{str(bulan_num).zfill(2)}",
                    "jumlah": int(pred)
                })

            # Update jendela rolling
            last_3.pop(0)
            last_3.append(pred)
            total_volume = sum(last_3)
            avg_3bulan = total_volume / 3
            flag_lonjakan = 1 if total_volume > 100 else 0

    return all_forecasts
