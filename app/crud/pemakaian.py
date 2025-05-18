from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.pemakaian import Pemakaian
from app.schemas.pemakaian import PemakaianIn, PemakaianRawCreate
from app.models.pemakaian_raw import PemakaianRaw

def tambah_pemakaian(db: Session, data: PemakaianIn):
    entry = Pemakaian(**data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def create_raw(db: Session, data: PemakaianRawCreate):
    record = PemakaianRaw(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_pemakaian(db: Session):
    return db.query(Pemakaian).all()

def aggregate_pemakaian_raw(db: Session, start_date: date, end_date: date):
    data = (
        db.query(
            PemakaianRaw.nama_obat.label("nama_obat"),
            func.strftime("%Y-%m", PemakaianRaw.tanggal).label("bulan"),
            func.sum(PemakaianRaw.volume).label("jumlah")
        )
        .filter(PemakaianRaw.tanggal >= start_date, PemakaianRaw.tanggal <= end_date)
        .group_by(PemakaianRaw.nama_obat, func.strftime("%Y-%m", PemakaianRaw.tanggal))
        .all()
    )

    inserted = 0
    for row in data:
        new_record = Pemakaian(
            namaobat=row.nama_obat,
            bulan=row.bulan + "-01",
            jumlah=row.jumlah
        )
        db.add(new_record)
        inserted += 1

    db.commit()
    return inserted
