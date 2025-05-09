from sqlalchemy.orm import Session
from models.stock import Stok
from schemas.stock import StokCreate

def tambah_stok(db: Session, data: StokCreate):
    stok = Stok(obat_id=data.obat_id, jumlah=data.jumlah)
    db.add(stok)
    db.commit()
    db.refresh(stok)
    return stok

def get_semua_stok(db: Session):
    return db.query(Stok).order_by(Stok.tanggal.desc()).all()
