from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StokCreate(BaseModel):
    obat_id: int
    jumlah: int

class StokOut(BaseModel):
    id: int
    obat_id: int
    jumlah: int
    tanggal: datetime

    class Config:
        orm_mode = True
