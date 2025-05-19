from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class PemakaianRaw(Base):
    __tablename__ = "pemakaian_raw"

    id = Column(Integer, primary_key=True, index=True)
    tanggal = Column(Date, index=True)
    nama_obat = Column(String, index=True)
    penyakit = Column(String)
    merk = Column(String)
    pabrik=Column(String)
    jenis = Column(String)  # Tablet, Kapsul, dll
    volume = Column(Integer)
