# ml_pipeline/src/models/train_catboost_v2_inference.py

"""
Treinamento do CatBoost V2 — MODELO INFERÍVEL
(Sem target leakage e sem proxies impossíveis)
"""

import joblib
from pathlib import Path

from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
)
from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def train_catboost_v2_inference():
    logger.info("Iniciando treino do CatBoost V2 INFERÍVEL")

    # =========================
    # Leitura dos dados
    # =========================
    train_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "train.parquet")
    val_df   = read_parquet(DATA_PROCESSED_DIR / "v2" / "validation.parquet")

    # =========================
    # Separação target
    # =========================
    y_train = train_df[TARGET_COLUMN]
    y_val   = val_df[TARGET_COLUMN]

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    X_val   = val_df.drop(columns=[TARGET_COLUMN])

    # =========================
    # REMOÇÕES CRÍTICAS (CORREÇÃO)
    # =========================
    forbidden_cols = [
        "log_renda_mensal_ocupacao_principal_deflacionado",
        "id_domicilio",
    ]

    for col in forbidden_cols:
        if col in X_train.columns:
            logger.warning(f"Removendo coluna proibida do treino: {col}")
            X_train = X_train.drop(columns=[col])
            X_val   = X_val.drop(columns=[col])

    # =========================
    # Features categóricas
    # =========================
    cat_features = X_train.select_dtypes(include=["object"]).columns.tolist()

    logger.info(f"Features categóricas ({len(cat_features)}): {cat_features}")
    logger.info(f"Total de features finais: {X_train.shape[1]}")

    # =========================
    # Modelo
    # =========================
    model = CatBoostRegressor(
        iterations=500,
        learning_rate=0.05,
        depth=8,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=42,
        verbose=False
    )

    # =========================
    # Treinamento
    # =========================
    model.fit(
        X_train,
        y_train,
        eval_set=(X_val, y_val),
        cat_features=cat_features,
        use_best_model=True
    )

    # =========================
    # Avaliação
    # =========================
    preds = model.predict(X_val)

    rmse = mean_squared_error(y_val, preds) ** 0.5
    mae  = mean_absolute_error(y_val, preds)
    r2   = r2_score(y_val, preds)

    logger.info(f"[VAL] RMSE: {rmse:.4f}")
    logger.info(f"[VAL] MAE : {mae:.4f}")
    logger.info(f"[VAL] R²  : {r2:.4f}")

    # =========================
    # Salvamento
    # =========================
    output_path = Path("models") / "catboost_v2_inference.joblib"
    joblib.dump(model, output_path)

    logger.info(f"Modelo inferível salvo em: {output_path}")

    # =========================
    # CHECK FINAL (CRÍTICO)
    # =========================
    logger.info("Verificando features finais do modelo...")
    logger.info(model.feature_names_)

    return model


if __name__ == "__main__":
    train_catboost_v2_inference()
