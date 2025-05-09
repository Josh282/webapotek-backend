
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pemakaian import Pemakaian

def import_csv_to_pemakaian():
    db: Session = SessionLocal()
    df = pd.read_csv("app/ml/dataset_obat_aggregated.csv")
    for _, row in df.iterrows():
        item = Pemakaian(
            obat_id=int(row["obat_id"]),
            jumlah=int(row["jumlah"]),
            bulan=pd.to_datetime(row["bulan"]).date()
        )
        db.add(item)
    db.commit()
    db.close()
    print("✅ Data dari CSV berhasil dimasukkan ke tabel pemakaian")

if __name__ == "__main__":
    import_csv_to_pemakaian()
