from sqlalchemy import Column, Integer, String
from database import Base

class Penyakit(Base):
    __tablename__ = "penyakit"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, unique=True, index=True)
