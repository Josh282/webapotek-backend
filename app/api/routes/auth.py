from fastapi import APIRouter, HTTPException, Depends
from app.schemas import user as schema
from app.crud import user as crud
from app.core.security import create_access_token
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.crud.user import authenticate_user
from app.schemas.auth import AuthRequest, AuthResponse

router = APIRouter()

@router.post("/register")
def register(data: schema.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered"}

@router.post("/login", response_model=AuthResponse)
def login(data: AuthRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username, "role": user.role})
    return AuthResponse(access_token=token, role=user.role)
