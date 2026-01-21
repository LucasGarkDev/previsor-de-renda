# ml_pipeline/src/tests/baseline_sanity_check_v2.py

"""
Teste sanitário (baseline ingênua)
Compara o modelo contra previsões constantes:
- média da renda
- mediana da renda
"""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
)
from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def run_baseline_sanity_check():
    logger.info("Iniciando TESTE SANITÁRIO — Baselines Ingênuas")

    train_path = DATA_PROCESSED_DIR / "v2" / "train.parquet"
    test_path = DATA_PROCESSED_DIR / "v2" / "test.parquet"

    df_train = read_parquet(train_path)
    df_test = read_parquet(test_path)

    y_train = df_train[TARGET_COLUMN]
    y_test = df_test[TARGET_COLUMN]

    # =========================
    # Baselines
    # =========================
    mean_pred = y_train.mean()
    median_pred = y_train.median()

    baselines = {
        "media": np.full(len(y_test), mean_pred),
        "mediana": np.full(len(y_test), median_pred),
    }

    for name, preds in baselines.items():
        rmse = mean_squared_error(y_test, preds) ** 0.5
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        logger.info(f"[BASELINE — {name.upper()}]")
        logger.info(f"Valor previsto: {mean_pred:.2f}" if name == "media" else f"Valor previsto: {median_pred:.2f}")
        logger.info(f"RMSE: {rmse:.4f}")
        logger.info(f"MAE : {mae:.4f}")
        logger.info(f"R²  : {r2:.4f}")
        logger.info("-" * 50)


if __name__ == "__main__":
    run_baseline_sanity_check()