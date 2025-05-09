# init_db.py
from database import Base, engine
from models import user, obat, stock, penyakit, pemakaian

Base.metadata.create_all(bind=engine)
