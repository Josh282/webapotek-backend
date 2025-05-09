from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from models.obat import Obat  # ✅ perbaikan di sini

class Pemakaian(Base):
    __tablename__ = "pemakaian"

    id = Column(Integer, primary_key=True, index=True)
    namaobat = Column(Integer, ForeignKey("obat.id"))
    jumlah = Column(Integer)
    bulan = Column(Date)

    obat = relationship("Obat")
