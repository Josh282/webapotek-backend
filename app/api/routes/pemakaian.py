from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.crud import pemakaian as crud
from app.schemas import pemakaian as schema
from typing import List
from datetime import date


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

@router.post("/manual", response_model=schema.PemakaianRawOut)
def input_pemakaian_manual(
    data: schema.PemakaianRawCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  # ✅ validasi token
):
    return crud.create_raw(db, data)

@router.post("/aggregate")
def aggregate_pemakaian(
    start_date: date = Query(..., description="Tanggal mulai (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Tanggal akhir (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  # ✅ validasi token
):
    inserted = crud.aggregate_pemakaian_raw(db, start_date, end_date)
    return {"message": "Agregasi selesai", "rows_inserted": inserted}

@router.get("/top15")
def top15_pemakaian(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud.get_top15_pemakaian_raw(db)

@router.get("/top5-penyakit")
def top5_penyakit_bulan_ini(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud.get_top5_penyakit_bulan_ini(db)


