# ml_pipeline/src/models/train_catboost_v2.py

"""
Treinamento do modelo CatBoost — versão v2
(Modelo final com variáveis domiciliares)
"""

import joblib
from pathlib import Path

from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    RANDOM_SEED,
)

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def train_catboost_v2():
    logger.info("Iniciando treino do CatBoost V2 (modelo contextual final)")

    # =========================
    # Leitura dos dados
    # =========================
    train_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "train.parquet")
    val_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "validation.parquet")

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_val = val_df.drop(columns=[TARGET_COLUMN])
    y_val = val_df[TARGET_COLUMN]

    # =========================
    # Identificação de categóricas
    # =========================
    categorical_features = X_train.select_dtypes(include=["object", "category"]).columns.tolist()

    logger.info(f"Features categóricas (CatBoost V2): {categorical_features}")
    logger.info(f"Total de features: {X_train.shape[1]}")

    # =========================
    # Tratamento de missing
    # =========================
    for col in categorical_features:
        X_train[col] = X_train[col].fillna("MISSING")
        X_val[col] = X_val[col].fillna("MISSING")

    # =========================
    # Modelo
    # =========================
    model = CatBoostRegressor(
        iterations=800,
        depth=6,
        learning_rate=0.05,
        loss_function="RMSE",
        random_seed=RANDOM_SEED,
        verbose=False,
    )

    # =========================
    # Treino
    # =========================
    model.fit(
        X_train,
        y_train,
        cat_features=categorical_features,
        eval_set=(X_val, y_val),
        early_stopping_rounds=50,
    )

    # =========================
    # Avaliação
    # =========================
    preds = model.predict(X_val)

    rmse = mean_squared_error(y_val, preds) ** 0.5
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)

    logger.info(f"CatBoost V2 RMSE (val): {rmse:.4f}")
    logger.info(f"CatBoost V2 MAE  (val): {mae:.4f}")
    logger.info(f"CatBoost V2 R²   (val): {r2:.4f}")

    # =========================
    # Persistência
    # =========================
    output_dir = Path("models")
    output_dir.mkdir(exist_ok=True)

    model_path = output_dir / "catboost_v2.joblib"
    joblib.dump(model, model_path)

    logger.info(f"Modelo CatBoost V2 salvo em: {model_path.resolve()}")

    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }


if __name__ == "__main__":
    train_catboost_v2()
