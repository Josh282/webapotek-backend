from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_db
from sqlalchemy.orm import Session
from models.penyakit import Penyakit
from models.obat import Obat

router = APIRouter()

@router.get("/mapping")
def get_dummy_mapping(db: Session = Depends(get_db)):
    # Dummy, nanti bisa ambil dari tabel relasi penyakit-obat
    return {
        "flu": ["Paracetamol", "Vitamin C"],
        "diare": ["Oralit", "Zinc Sulfate"]
    }
