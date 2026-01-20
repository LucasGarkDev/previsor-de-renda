import pandas as pd

from backend.app.schemas.predict import PredictInput
from backend.app.core.feature_builder import build_model_features
from backend.app.services.model_loader import ModelLoader


class PredictService:
    """
    Serviço responsável por executar a predição de renda.
    """

    @staticmethod
    def predict(input_data: PredictInput) -> float:
        # 1. Construir DataFrame de features
        features_df: pd.DataFrame = build_model_features(input_data)

        # 2. Obter modelo carregado
        model = ModelLoader.get_model()

        # 3. Executar predição
        prediction = model.predict(features_df)

        # 4. Retornar valor escalar
        return float(prediction[0])
