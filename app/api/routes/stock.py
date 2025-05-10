from fastapi import APIRouter, Depends
from app.api.dependencies import get_db
from app.crud import stock as crud
from app.schemas import stock as schema
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/", response_model=schema.StokOut)
def input_stok(data: schema.StokCreate, db: Session = Depends(get_db)):
    return crud.tambah_stok(db, data)

@router.get("/", response_model=List[schema.StokOut])
def get_stok(db: Session = Depends(get_db)):
    return crud.get_semua_stok(db)
