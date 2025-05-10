from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.crud import pemakaian as crud
from app.schemas import pemakaian as schema
from typing import List

router = APIRouter()

@router.post("/", response_model=schema.PemakaianOut)
def input_pemakaian(
    data: schema.PemakaianIn,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # ✅ validasi token
):
    return crud.tambah_pemakaian(db, data)

@router.get("/", response_model=List[schema.PemakaianOut])
def get_pemakaian(db: Session = Depends(get_db)):
    return crud.get_all_pemakaian(db)
