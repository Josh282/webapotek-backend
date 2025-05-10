from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Stok(Base):
    __tablename__ = "stok"

    id = Column(Integer, primary_key=True, index=True)
    obat_id = Column(Integer, ForeignKey("obat.id"))
    jumlah = Column(Integer)
    tanggal = Column(DateTime, default=datetime.utcnow)

    obat = relationship("Obat")
