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

        # Baca file sebagai excel atau csv
        if filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        elif filename.endswith(".csv"):
            decoded = contents.decode("utf-8")
            df = pd.read_csv(io.StringIO(decoded))
        else:
            raise HTTPException(status_code=400, detail="File harus .csv atau .xlsx")

        # Rename kolom agar match dengan field database
        df.rename(columns={
            "tgl_resep": "tanggal",
            "namaobat": "nama_obat",
            "Penyakit Utama": "penyakit",
            "pabrikan": "pabrik"
        }, inplace=True)

        # Validasi kolom wajib
        required_cols = {"tanggal", "nama_obat", "penyakit", "merk", "jenis", "pabrik", "volume"}
        if not required_cols.issubset(set(df.columns)):
            raise HTTPException(status_code=400, detail=f"File harus mengandung kolom: {', '.join(required_cols)}")

        # Pastikan format tanggal benar
        df["tanggal"] = pd.to_datetime(df["tanggal"]).dt.date

        # Simpan ke database
        for _, row in df.iterrows():
            db.add(PemakaianRaw(**row.to_dict()))
        db.commit()

        return {"message": f"Upload sukses: {file.filename}", "rows": len(df)}

    except Exception as e:
        print("❌ ERROR during upload:", e)
        raise HTTPException(status_code=400, detail=f"Upload gagal: {e}")
