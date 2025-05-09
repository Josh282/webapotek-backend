from pydantic import BaseModel
from datetime import date

class PemakaianIn(BaseModel):
    obat_id: int
    jumlah: int
    bulan: date

class PemakaianOut(PemakaianIn):
    id: int

    class Config:
        orm_mode = True
