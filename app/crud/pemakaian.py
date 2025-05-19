from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from datetime import date, datetime
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
        try:
            bulan_date = datetime.strptime(row.bulan + "-01", "%Y-%m-%d").date()
        except Exception as e:
            print("❌ Gagal konversi bulan:", row.bulan, "→", e)
            continue

        # ❗️Cek apakah record sudah ada
        existing = (
            db.query(Pemakaian)
            .filter(Pemakaian.namaobat == row.nama_obat, Pemakaian.bulan == bulan_date)
            .first()
        )
        if existing:
            continue  # Skip duplikat

        new_record = Pemakaian(
            namaobat=row.nama_obat,
            bulan=bulan_date,
            jumlah=row.jumlah
        )
        db.add(new_record)
        inserted += 1

    db.commit()
    return inserted


def get_top15_pemakaian_raw(db: Session):
    from sqlalchemy import func
    from app.models.pemakaian_raw import PemakaianRaw

    result = (
        db.query(
            PemakaianRaw.nama_obat,
            func.sum(PemakaianRaw.volume).label("total_volume")
        )
        .group_by(PemakaianRaw.nama_obat)
        .order_by(func.sum(PemakaianRaw.volume).desc())
        .limit(15)
        .all()
    )

    return [{"obat": r.nama_obat, "jumlah": int(r.total_volume)} for r in result]

def get_top5_penyakit_bulan_ini(db: Session):
    from app.models.pemakaian_raw import PemakaianRaw

    today = date.today()
    bulan = today.month
    tahun = today.year

    result = (
        db.query(
            PemakaianRaw.penyakit,
            func.sum(PemakaianRaw.volume).label("total")
        )
        .filter(
            extract("month", PemakaianRaw.tanggal) == bulan,
            extract("year", PemakaianRaw.tanggal) == tahun
        )
        .group_by(PemakaianRaw.penyakit)
        .order_by(func.sum(PemakaianRaw.volume).desc())
        .limit(5)
        .all()
    )

    return [{"penyakit": r.penyakit, "jumlah": int(r.total)} for r in result]
