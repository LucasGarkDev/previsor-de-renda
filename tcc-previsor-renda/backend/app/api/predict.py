#  backend/app/api/predict.py
from fastapi import APIRouter, HTTPException
from backend.app.schemas.predict import PredictInput, PredictOutput
from backend.app.services.predict_service import PredictService

router = APIRouter()

@router.post("/predict", response_model=PredictOutput)
def predict(payload: PredictInput):
    try:
        return PredictService.predict(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
