from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
from app.models.pemakaian import Pemakaian
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", tags=["Upload"])
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        decoded = contents.decode("utf-8")
        df = pd.read_csv(io.StringIO(decoded))

        required_cols = {"namaobat", "total_volume", "bulan"}
        if not required_cols.issubset(set(df.columns)):
            raise HTTPException(status_code=400, detail="CSV harus mengandung kolom: namaobat, total_volume, bulan")

        for _, row in df.iterrows():
            db.add(Pemakaian(
                namaobat=row["namaobat"],
                jumlah=int(row["total_volume"]),
                bulan=pd.to_datetime(row["bulan"]).date()
            ))

        db.commit()
        return {"message": f"Upload sukses: {file.filename}", "rows": len(df)}

    except Exception as e:
        print("❌ ERROR during upload:", e)
        raise HTTPException(status_code=400, detail=f"Upload gagal: {e}")
