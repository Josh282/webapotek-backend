from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.obat import Obat
from app.models.penyakit import Penyakit

# List data awal
obat_list = [
    "Paracetamol", "Amoxicillin", "Ibuprofen", "Antibiotik", "Vit C"
]

penyakit_list = [
    "Demam", "Infeksi", "Radang", "Batuk", "Flu"
]

def seed_obat(db: Session):
    for name in obat_list:
        exists = db.query(Obat).filter_by(nama=name).first()
        if not exists:
            db.add(Obat(nama=name))
    db.commit()

def seed_penyakit(db: Session):
    for name in penyakit_list:
        exists = db.query(Penyakit).filter_by(nama=name).first()
        if not exists:
            db.add(Penyakit(nama=name))
    db.commit()

def run():
    db = SessionLocal()
    seed_obat(db)
    seed_penyakit(db)
    db.close()
    print("✅ Seeder berhasil dijalankan!")

if __name__ == "__main__":
    run()
