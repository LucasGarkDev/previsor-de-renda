# backend/app/services/model_loader.py
from pathlib import Path
import joblib
from catboost import CatBoostRegressor

MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "models"
    / "catboost_v2_inference.joblib"
)

class ModelLoader:
    _model: CatBoostRegressor | None = None

    @classmethod
    def get_model(cls) -> CatBoostRegressor:
        if cls._model is None:
            cls._model = cls._load_model()
        return cls._model

    @staticmethod
    def _load_model() -> CatBoostRegressor:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {MODEL_PATH}")
        return joblib.load(MODEL_PATH)
