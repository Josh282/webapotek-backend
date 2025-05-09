from app.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def create_demo_user():
    db = SessionLocal()
    username = "admin"
    password = "admin"
    role = "admin"

    user = db.query(User).filter_by(username=username).first()
    if user:
        print("✅ User admin sudah ada.")
    else:
        new_user = User(username=username, hashed_password=hash_password(password), role=role)
        db.add(new_user)
        db.commit()
        print("✅ User admin berhasil dibuat.")
    db.close()

if __name__ == "__main__":
    create_demo_user()
