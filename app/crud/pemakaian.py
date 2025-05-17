from sqlalchemy.orm import Session
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
