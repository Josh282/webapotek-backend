from sqlalchemy import Column, Integer, String
from app.database import Base

class Obat(Base):
    __tablename__ = "obat"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, unique=True, index=True)
    satuan = Column(String, default="tablet")
