from fastapi import APIRouter
from backend.app.schemas.predict import PredictInput
from backend.app.services.predict_service import PredictService

router = APIRouter()

@router.post("/predict")
def predict(payload: PredictInput):
    return PredictService.predict(payload)
