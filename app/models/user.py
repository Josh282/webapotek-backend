from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="admin") 
