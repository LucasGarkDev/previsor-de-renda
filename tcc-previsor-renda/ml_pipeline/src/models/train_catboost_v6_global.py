"""
Treinamento CatBoost V6 — GLOBAL
Dataset: v3 + Feature Engineering V6
(Log Target + Smearing Correction)
"""

import joblib
import numpy as np
from pathlib import Path

from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    RANDOM_SEED,
    USE_LOG1P,
    ENABLE_SMEARING,
)

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def _log_transform(y):
    return np.log1p(y) if USE_LOG1P else np.log(y)


def _inverse_log(y_log):
    return np.expm1(y_log) if USE_LOG1P else np.exp(y_log)


def train_catboost_v6_global():

    logger.info("Iniciando treino CatBoost V6 — GLOBAL")

    # =========================
    # Leitura dos dados (V6)
    # =========================
    train_df = read_parquet(DATA_PROCESSED_DIR / "v3" / "train.parquet")
    val_df = read_parquet(DATA_PROCESSED_DIR / "v3" / "validation.parquet")

    logger.info(f"Train size: {len(train_df)}")
    logger.info(f"Validation size: {len(val_df)}")

    # =========================
    # Separação target
    # =========================
    y_train_raw = train_df[TARGET_COLUMN]
    y_val_raw = val_df[TARGET_COLUMN]

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    X_val = val_df.drop(columns=[TARGET_COLUMN])

    # =========================
    # Remover colunas proibidas
    # =========================
    forbidden_cols = [
        "log_renda_mensal_ocupacao_principal_deflacionado",
        "id_domicilio",
    ]

    for col in forbidden_cols:
        if col in X_train.columns:
            X_train = X_train.drop(columns=[col])
            X_val = X_val.drop(columns=[col])

    # =========================
    # Log transform
    # =========================
    y_train = _log_transform(y_train_raw)
    y_val = _log_transform(y_val_raw)

    # =========================
    # Tratamento categóricas
    # =========================
    cat_features = X_train.select_dtypes(include=["object"]).columns.tolist()

    for col in cat_features:
        X_train[col] = X_train[col].astype(str).fillna("NA")
        X_val[col] = X_val[col].astype(str).fillna("NA")

    X_train = X_train.fillna(-999)
    X_val = X_val.fillna(-999)

    logger.info(f"Total features: {X_train.shape[1]}")
    logger.info(f"Categóricas: {cat_features}")

    # =========================
    # Modelo
    # =========================
    model = CatBoostRegressor(
        iterations=2000,
        learning_rate=0.03,
        depth=8,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=RANDOM_SEED,
        early_stopping_rounds=100,
        verbose=200,
    )

    model.fit(
        X_train,
        y_train,
        cat_features=cat_features,
        eval_set=(X_val, y_val),
        use_best_model=True,
    )

    # =========================
    # Smearing
    # =========================
    smearing_factor = 1.0

    if ENABLE_SMEARING:
        residuals = y_train - model.predict(X_train)
        smearing_factor = np.mean(np.exp(residuals))

    # =========================
    # Avaliação
    # =========================
    val_preds = _inverse_log(model.predict(X_val)) * smearing_factor

    rmse = mean_squared_error(y_val_raw, val_preds) ** 0.5
    mae = mean_absolute_error(y_val_raw, val_preds)
    r2 = r2_score(y_val_raw, val_preds)

    logger.info(f"[VAL V6 GLOBAL] RMSE: {rmse:.4f}")
    logger.info(f"[VAL V6 GLOBAL] MAE : {mae:.4f}")
    logger.info(f"[VAL V6 GLOBAL] R²  : {r2:.4f}")

    # =========================
    # Salvar modelo
    # =========================
    Path("models").mkdir(exist_ok=True)

    bundle = {
        "model": model,
        "cat_features": cat_features,
        "smearing_factor": smearing_factor,
        "metrics": {"rmse": rmse, "mae": mae, "r2": r2},
        "version": "V6",
    }

    joblib.dump(bundle, "models/catboost_v6_global.joblib")

    logger.info("Modelo V6 salvo com sucesso.")

    return bundle


if __name__ == "__main__":
    train_catboost_v6_global()