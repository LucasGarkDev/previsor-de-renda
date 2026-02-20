"""
Análise de Feature Importance — Modelo V5 Global

Objetivo:
- Carregar modelo salvo
- Extrair importância das features
- Exibir Top 10
- Calcular importância percentual
"""

import joblib
import pandas as pd
from pathlib import Path
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


MODEL_PATH = Path("models/catboost_v5_global.joblib")


def analyze_feature_importance():

    logger.info("Carregando modelo V5...")

    bundle = joblib.load(MODEL_PATH)

    model = bundle["model"]

    logger.info("Extraindo feature importance...")

    importance_df = model.get_feature_importance(prettified=True)

    # Normalizar para percentual
    total_importance = importance_df["Importances"].sum()
    importance_df["Importance_%"] = (
        importance_df["Importances"] / total_importance * 100
    )

    # Ordenar
    importance_df = importance_df.sort_values(
        by="Importances", ascending=False
    )

    logger.info("Top 10 variáveis mais importantes:")
    print("\n========== TOP 10 FEATURES ==========\n")
    print(importance_df.head(10).to_string(index=False))

    print("\n========== IMPORTÂNCIA TOTAL (%) ==========\n")
    print(importance_df.head(10)[["Feature Id", "Importance_%"]].to_string(index=False))

    return importance_df


if __name__ == "__main__":
    analyze_feature_importance()