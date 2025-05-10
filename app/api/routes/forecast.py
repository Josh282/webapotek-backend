from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.ml.predictor import predict_from_pemakaian

router = APIRouter()

@router.get("/")
def get_forecast(
    horizon: int = Query(1, ge=1, le=12, description="Jumlah bulan ke depan untuk prediksi"),
    db: Session = Depends(get_db)
):
    try:
        hasil = predict_from_pemakaian(db, horizon=horizon)
        return {"forecast": hasil}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast failed: {str(e)}")
