from pathlib import Path
import joblib
from catboost import CatBoostRegressor


# Caminho absoluto para o modelo
MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "catboost_v2_no_id.joblib"


class ModelLoader:
    """
    Responsável por carregar e fornecer acesso ao modelo treinado.
    Implementa um padrão simples de singleton.
    """

    _model: CatBoostRegressor | None = None

    @classmethod
    def get_model(cls) -> CatBoostRegressor:
        if cls._model is None:
            cls._model = cls._load_model()
        return cls._model

    @staticmethod
    def _load_model() -> CatBoostRegressor:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Modelo não encontrado em: {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)

        if not isinstance(model, CatBoostRegressor):
            raise TypeError("O arquivo carregado não é um CatBoostRegressor.")

        return model
