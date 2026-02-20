# ml_pipeline/src/models/evaluate_model_v4_smearing.py

"""
Avaliação FINAL dos modelos V4 (Log + Smearing)
Avalia já na escala original da renda.
"""

import numpy as np
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
)

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.models.predict_smearing import load_bundle, predict_income

logger = get_logger(__name__)


def evaluate_model_v4_smearing(model_name: str):

    logger.info(f"Iniciando avaliação V4: {model_name}")

    model_path = Path("models") / f"{model_name}.joblib"
    test_path = DATA_PROCESSED_DIR / "v2" / "test.parquet"

    # =========================
    # Carregar dados
    # =========================
    df_test = read_parquet(test_path)
    y_test = df_test[TARGET_COLUMN]

    X_test = df_test.drop(columns=[TARGET_COLUMN])

    # =========================
    # Carregar modelo
    # =========================
    bundle = load_bundle(model_path)

    # =========================
    # Predição
    # =========================
    preds = predict_income(bundle, X_test)

    # =========================
    # Métricas
    # =========================
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    logger.info(f"[TEST V4] {model_name}")
    logger.info(f"RMSE: {rmse:.4f}")
    logger.info(f"MAE : {mae:.4f}")
    logger.info(f"R²  : {r2:.4f}")

    return {
        "model": model_name,
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }


if __name__ == "__main__":
    evaluate_model_v4_smearing("catboost_v5_global")