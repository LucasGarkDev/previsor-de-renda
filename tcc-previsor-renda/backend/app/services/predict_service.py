from __future__ import annotations

import math

from backend.app.core.feature_builder import build_model_features
from backend.app.schemas.predict import PredictInput
from backend.app.services.model_loader import ModelLoader

MAE_HYBRID = 528.32
SIGMA_LOG_HYBRID = 0.5737
INTERVAL_Z_SCORE = 1.96


class PredictService:
    @staticmethod
    def predict(input_data: PredictInput) -> dict:
        features_df = build_model_features(input_data)
        bundle = ModelLoader.get_bundle()

        mincer_features = features_df[
            [
                "anos_estudo",
                "experiencia_aprox",
                "idade_quadrado",
                "sexo",
                "regiao",
                "possui_carteira_assinada",
            ]
        ]

        residual_features = features_df[bundle.residual_model.feature_names_].copy()
        categorical_features = residual_features.select_dtypes(include=["object", "category"]).columns.tolist()
        for column in categorical_features:
            residual_features[column] = residual_features[column].astype(str).fillna("MISSING")

        mincer_prediction = float(bundle.mincer_model.predict(mincer_features)[0])
        residual_prediction = float(bundle.residual_model.predict(residual_features)[0])
        predicted_log_income = mincer_prediction + residual_prediction

        renda_estimada = math.exp(predicted_log_income) * bundle.smearing_factor
        intervalo_min = math.exp(predicted_log_income - INTERVAL_Z_SCORE * SIGMA_LOG_HYBRID) * bundle.smearing_factor
        intervalo_max = math.exp(predicted_log_income + INTERVAL_Z_SCORE * SIGMA_LOG_HYBRID) * bundle.smearing_factor

        return {
            "renda_estimada": round(renda_estimada, 2),
            "intervalo_provavel": {
                "min": round(max(0, intervalo_min), 2),
                "max": round(intervalo_max, 2),
            },
            "erro_medio_modelo": MAE_HYBRID,
            "observacao": (
                "Estimativa gerada pelo modelo hibrido Mincer + CatBoost residual, "
                "com retransformacao via smearing. O intervalo provavel e calculado "
                "na escala logaritmica e convertido para renda mensal na escala original."
            ),
        }
