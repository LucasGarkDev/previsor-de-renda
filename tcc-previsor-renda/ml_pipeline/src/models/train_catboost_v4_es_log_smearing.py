# ml_pipeline/src/models/train_catboost_v4_es_log_smearing.py

"""
Treinamento CatBoost V4 — Segmento Espírito Santo (ES)
(Log Target + Smearing Correction)

Modelo especializado apenas para registros do ES.
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
    UF_COLUMN,
    USE_LOG1P,
    ENABLE_SMEARING,
)

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


UF_FOCUS = "ES"


def _log_transform(y):
    if USE_LOG1P:
        return np.log1p(y)
    return np.log(y)


def _inverse_log(y_log):
    if USE_LOG1P:
        return np.expm1(y_log)
    return np.exp(y_log)


def train_catboost_v4_es_log_smearing():

    logger.info("Iniciando treino CatBoost V4 — ES (Log + Smearing)")

    # =========================
    # Leitura
    # =========================
    train_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "train.parquet")
    val_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "validation.parquet")

    # =========================
    # Filtro ES obrigatório
    # =========================
    train_df = train_df[train_df[UF_COLUMN] == UF_FOCUS].copy()
    val_df = val_df[val_df[UF_COLUMN] == UF_FOCUS].copy()

    logger.info(f"Treino ES: {len(train_df)} registros")
    logger.info(f"Validação ES: {len(val_df)} registros")

    if len(train_df) < 50:
        logger.warning("⚠️ Dataset ES muito pequeno. Métricas podem ser instáveis.")

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
            logger.warning(f"Removendo coluna proibida: {col}")
            X_train = X_train.drop(columns=[col])
            X_val = X_val.drop(columns=[col])

    # =========================
    # Log-transform do target
    # =========================
    y_train = _log_transform(y_train_raw)
    y_val = _log_transform(y_val_raw)

    # =========================
    # Features categóricas
    # =========================
    cat_features = X_train.select_dtypes(include=["object"]).columns.tolist()

    logger.info(f"Total features: {X_train.shape[1]}")
    logger.info(f"Features categóricas: {cat_features}")

    # =========================
    # Modelo
    # =========================
    model = CatBoostRegressor(
        iterations=1000,
        learning_rate=0.03,
        depth=8,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=RANDOM_SEED,
        early_stopping_rounds=50,
        verbose=False,
    )

    # =========================
    # Treinamento
    # =========================
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
        logger.info("Calculando smearing factor (ES)...")
        train_preds_log = model.predict(X_train)
        residuals = y_train - train_preds_log
        smearing_factor = np.mean(np.exp(residuals))
        logger.info(f"Smearing factor ES: {smearing_factor:.6f}")

    # =========================
    # Avaliação em escala real
    # =========================
    val_preds_log = model.predict(X_val)
    val_preds = _inverse_log(val_preds_log) * smearing_factor

    rmse = mean_squared_error(y_val_raw, val_preds) ** 0.5
    mae = mean_absolute_error(y_val_raw, val_preds)
    r2 = r2_score(y_val_raw, val_preds)

    logger.info(f"[VAL V4 ES] RMSE: {rmse:.4f}")
    logger.info(f"[VAL V4 ES] MAE : {mae:.4f}")
    logger.info(f"[VAL V4 ES] R²  : {r2:.4f}")

    # =========================
    # Salvamento
    # =========================
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_filename = "catboost_v4_es.joblib"
    output_path = models_dir / model_filename

    bundle = {
        "model": model,
        "feature_names": model.feature_names_,
        "cat_features": cat_features,
        "smearing_factor": smearing_factor,
        "use_log1p": USE_LOG1P,
        "segment": "ES",
        "metrics": {
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
        },
    }

    joblib.dump(bundle, output_path)

    logger.info(f"Modelo ES salvo em: {output_path.resolve()}")

    return bundle


if __name__ == "__main__":
    train_catboost_v4_es_log_smearing()