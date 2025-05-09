from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PredictRequest(BaseModel):
    features: list

class PredictResponse(BaseModel):
    prediction: list

@router.post("/", response_model=PredictResponse)
def run_prediction(request: PredictRequest):
    result = predict(request.features)
    return PredictResponse(prediction=result)
