from sqlalchemy.orm import Session
from app.models.pemakaian import Pemakaian
from app.schemas.pemakaian import PemakaianIn

def tambah_pemakaian(db: Session, data: PemakaianIn):
    entry = Pemakaian(**data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_all_pemakaian(db: Session):
    return db.query(Pemakaian).all()
