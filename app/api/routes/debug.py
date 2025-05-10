from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.user import User

router = APIRouter()

@router.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return [{"username": u.username, "role": u.role} for u in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
