from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
from app.api.dependencies import get_db
from app.models.pemakaian_raw import PemakaianRaw

router = APIRouter()

@router.post("/", tags=["Upload"])
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        filename = file.filename.lower()

        # Baca file sebagai Excel atau CSV
        if filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        elif filename.endswith(".csv"):
            decoded = contents.decode("utf-8")
            df = pd.read_csv(io.StringIO(decoded))
        else:
            raise HTTPException(status_code=400, detail="File harus .csv atau .xlsx")

        # Rename kolom agar sesuai dengan field database
        df.rename(columns={
            "tgl_resep": "tanggal",
            "namaobat": "nama_obat",
            "Penyakit Utama": "penyakit",
            "pabrikan": "pabrik"
        }, inplace=True)

        # Ambil hanya kolom yang dibutuhkan
        required_cols = ["tanggal", "nama_obat", "penyakit", "merk", "jenis", "pabrik", "volume"]
        df = df.loc[:, df.columns.intersection(required_cols)]

        # Validasi apakah semua kolom ada
        if set(required_cols) - set(df.columns):
            missing = set(required_cols) - set(df.columns)
            raise HTTPException(
                status_code=400,
                detail=f"File tidak lengkap, kolom kurang: {', '.join(missing)}"
            )

        # Pastikan format tanggal valid
        df["tanggal"] = pd.to_datetime(df["tanggal"]).dt.date

        # Simpan ke database
        for _, row in df.iterrows():
            db.add(PemakaianRaw(**row.to_dict()))
        db.commit()

        return {"message": f"Upload sukses: {file.filename}", "rows": len(df)}

    except Exception as e:
        print("❌ ERROR during upload:", e)
        raise HTTPException(status_code=400, detail=f"Upload gagal: {e}")
