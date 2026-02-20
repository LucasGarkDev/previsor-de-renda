# ml_pipeline/src/models/train_catboost_v4_log_smearing.py

"""
Treinamento CatBoost V4 — Log Target + Smearing Correction

Estratégia:
- Treinar modelo no log da renda
- Aplicar correção de smearing para remover viés da exponenciação
- Suporte a segmentação (UF / urbano)
- Salvar bundle completo com metadata

Modelo resultante:
- models/catboost_v4_<segment>.joblib
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
    ENABLE_UF_FILTER,
    UF_WHITELIST,
    ENABLE_URBAN_ONLY,
    URBAN_COLUMN,
    UF_COLUMN,
    USE_LOG1P,
    ENABLE_SMEARING,
    MODEL_SEGMENT_NAME,
)

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def _apply_segment_filters(df):
    """Aplica filtros por UF e urbano conforme settings."""
    original_len = len(df)

    if ENABLE_UF_FILTER:
        df = df[df[UF_COLUMN].isin(UF_WHITELIST)].copy()
        logger.info(f"Filtro UF aplicado: {UF_WHITELIST}")

    if ENABLE_URBAN_ONLY:
        df = df[df[URBAN_COLUMN] == 1].copy()
        logger.info("Filtro urbano aplicado (zona_urbana == 1)")

    logger.info(f"Registros após filtros: {len(df)} (antes: {original_len})")
    return df


def _log_transform(y):
    if USE_LOG1P:
        return np.log1p(y)
    return np.log(y)


def _inverse_log(y_log):
    if USE_LOG1P:
        return np.expm1(y_log)
    return np.exp(y_log)


def train_catboost_v4_log_smearing():

    logger.info("Iniciando treino CatBoost V5 — Log + Smearing")

    # =========================
    # Leitura dos dados
    # =========================
    train_path = DATA_PROCESSED_DIR / "v3" / "train.parquet"
    val_path = DATA_PROCESSED_DIR / "v3" / "validation.parquet"

    # =========================
    # Aplicar segmentação
    # =========================
    train_df = _apply_segment_filters(train_df)
    val_df = _apply_segment_filters(val_df)

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
    # Smearing factor
    # =========================
    smearing_factor = 1.0

    if ENABLE_SMEARING:
        logger.info("Calculando smearing factor...")
        train_preds_log = model.predict(X_train)
        residuals = y_train - train_preds_log
        smearing_factor = np.mean(np.exp(residuals))
        logger.info(f"Smearing factor: {smearing_factor:.6f}")

    # =========================
    # Avaliação (já na escala original)
    # =========================
    val_preds_log = model.predict(X_val)
    val_preds = _inverse_log(val_preds_log) * smearing_factor

    rmse = mean_squared_error(y_val_raw, val_preds) ** 0.5
    mae = mean_absolute_error(y_val_raw, val_preds)
    r2 = r2_score(y_val_raw, val_preds)

    logger.info(f"[VAL V5] RMSE: {rmse:.4f}")
    logger.info(f"[VAL V5] MAE : {mae:.4f}")
    logger.info(f"[VAL V5] R²  : {r2:.4f}")

    # =========================
    # Salvamento (bundle completo)
    # =========================
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_filename = f"catboost_v5_{MODEL_SEGMENT_NAME}.joblib"
    output_path = models_dir / model_filename

    bundle = {
        "model": model,
        "feature_names": model.feature_names_,
        "cat_features": cat_features,
        "smearing_factor": smearing_factor,
        "use_log1p": USE_LOG1P,
        "segment": MODEL_SEGMENT_NAME,
        "metrics": {
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
        },
    }

    joblib.dump(bundle, output_path)

    logger.info(f"Modelo V4 salvo em: {output_path.resolve()}")

    return bundle


if __name__ == "__main__":
    train_catboost_v4_log_smearing()