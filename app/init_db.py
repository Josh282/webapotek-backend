# init_db.py
from app.database import Base, engine
from app.models import user, obat, stock, penyakit, pemakaian

Base.metadata.create_all(bind=engine)
