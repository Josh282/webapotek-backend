from sqlalchemy.orm import Session
from app.models.penyakit import Penyakit

def get_all_penyakit(db: Session):
    return db.query(Penyakit).all()

def get_penyakit_by_id(db: Session, id: int):
    return db.query(Penyakit).filter(Penyakit.id == id).first()

def create_penyakit(db: Session, nama: str):
    penyakit = Penyakit(nama=nama)
    db.add(penyakit)
    db.commit()
    db.refresh(penyakit)
    return penyakit
