from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.ml.predictor import predict_from_pemakaian
from app.core.security import verify_token  # ✅ Verifikasi JWT token

router = APIRouter()
security = HTTPBearer()

@router.get("")
def get_forecast(
    horizon: int = Query(1, ge=1, le=12, description="Jumlah bulan ke depan untuk prediksi"),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    verify_token(credentials.credentials)
    try:
        hasil = predict_from_pemakaian(db, horizon=horizon)
        top15 = sorted(hasil, key=lambda x: x["jumlah"], reverse=True)[:15]
        return {"forecast": hasil}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast failed: {str(e)}")

@router.get("/top15")
def get_top15_forecast(
    horizon: int = Query(1, ge=1, le=12),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    verify_token(credentials.credentials)
    try:
        hasil = predict_from_pemakaian(db, horizon=horizon)
        hasil_sorted = sorted(hasil, key=lambda x: x["jumlah"], reverse=True)[:15]
        return {"forecast_top15": hasil_sorted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Top15 Forecast Error: {str(e)}")
