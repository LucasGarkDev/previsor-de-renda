import pandas as pd

from backend.app.schemas.predict import PredictInput
from backend.app.core.feature_builder import build_model_features
from backend.app.services.model_loader import ModelLoader


class PredictService:
    @staticmethod
    def predict(input_data: PredictInput) -> dict:
        features_df = build_model_features(input_data)
        model = ModelLoader.get_model()

        y_hat = float(model.predict(features_df)[0])

        # valores vindos da avaliação do modelo
        MAE_TESTE = 1500.0
        Q90_ERRO = 3800.0

        return {
            "renda_estimada": round(y_hat, 2),
            "intervalo_provavel": {
                "min": round(max(0, y_hat - Q90_ERRO), 2),
                "max": round(y_hat + Q90_ERRO, 2),
            },
            "erro_medio_modelo": MAE_TESTE,
            "observacao": (
                "O erro médio representa o desempenho global do modelo "
                "no conjunto de teste. A renda real pode variar por fatores "
                "não observados."
            ),
        }
