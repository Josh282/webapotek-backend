from pydantic import BaseModel
from datetime import date
from typing import Optional

class PemakaianIn(BaseModel):
    obat_id: int
    jumlah: int
    bulan: date

class PemakaianOut(PemakaianIn):
    id: int

    class Config:
        orm_mode = True

class PemakaianRawCreate(BaseModel):
    tanggal: date
    nama_obat: str
    penyakit: Optional[str] = None
    jenis: Optional[str] = None
    merk: Optional[str] = None
    pabrik: Optional[str] = None
    volume: int

class PemakaianRawOut(PemakaianRawCreate):
    id: int

    class Config:
        orm_mode = True
