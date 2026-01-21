# ml_pipeline/src/tests/train_catboost_v2_log_target.py

import numpy as np
import joblib
from catboost import CatBoostRegressor

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
)
from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)

PROIBIDAS = {
    TARGET_COLUMN,
    f"log_{TARGET_COLUMN}",
    "id_domicilio",
}

def train_catboost_v2_log_target():
    logger.info("Iniciando treino do CatBoost V2 com alvo log1p(renda)")

    train_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "train.parquet")
    val_df   = read_parquet(DATA_PROCESSED_DIR / "v2" / "validation.parquet")

    # =========================
    # Target logarítmico
    # =========================
    y_train = np.log1p(train_df[TARGET_COLUMN])
    y_val   = np.log1p(val_df[TARGET_COLUMN])

    # =========================
    # Features inferíveis
    # =========================
    X_train = train_df.drop(columns=[c for c in PROIBIDAS if c in train_df.columns])
    X_val   = val_df.drop(columns=[c for c in PROIBIDAS if c in val_df.columns])

    # =========================
    # Categóricas
    # =========================
    cat_features = X_train.select_dtypes(include=["object"]).columns.tolist()

    logger.info(f"Features categóricas ({len(cat_features)}): {cat_features}")
    logger.info(f"Total de features: {X_train.shape[1]}")

    model = CatBoostRegressor(
        iterations=500,
        depth=8,
        learning_rate=0.05,
        loss_function="RMSE",
        random_seed=42,
        verbose=False,
    )

    model.fit(
        X_train,
        y_train,
        eval_set=(X_val, y_val),
        cat_features=cat_features,
        use_best_model=True,
    )

    joblib.dump(model, "models/catboost_v2_log_target.joblib")

    logger.info("Modelo salvo em models/catboost_v2_log_target.joblib")
    logger.info(f"Features finais: {model.feature_names_}")

if __name__ == "__main__":
    train_catboost_v2_log_target()
