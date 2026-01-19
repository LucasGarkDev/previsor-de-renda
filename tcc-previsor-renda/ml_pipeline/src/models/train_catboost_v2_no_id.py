# ml_pipeline/src/models/train_catboost_v2_no_id.py

import joblib
from pathlib import Path

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    RANDOM_SEED,
)

from ml_pipeline.src.models.modelsList import MODEL_REGISTRY

logger = get_logger(__name__)


def train_catboost_v2_no_id():
    model_name = "catboost_v2_no_id"
    logger.info("Iniciando treino do CatBoost V2 SEM id_domicilio")

    # =========================
    # Leitura dos dados
    # =========================
    train_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "train.parquet")
    val_df = read_parquet(DATA_PROCESSED_DIR / "v2" / "validation.parquet")

    # =========================
    # Separação X / y
    # =========================
    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_val = val_df.drop(columns=[TARGET_COLUMN])
    y_val = val_df[TARGET_COLUMN]

    # =========================
    # REMOÇÃO CRÍTICA
    # =========================
    if "id_domicilio" in X_train.columns:
        logger.warning("Removendo variável id_domicilio para evitar proxy leakage")
        X_train = X_train.drop(columns=["id_domicilio"])
        X_val = X_val.drop(columns=["id_domicilio"])

    # =========================
    # Identificação de categóricas
    # =========================
    categorical_features = X_train.select_dtypes(
        include=["object"]
    ).columns.tolist()

    logger.info(f"Features categóricas (sem id): {categorical_features}")
    logger.info(f"Total de features: {X_train.shape[1]}")

    # =========================
    # Tratamento de missing em categóricas
    # =========================
    for col in categorical_features:
        X_train[col] = X_train[col].fillna("MISSING")
        X_val[col] = X_val[col].fillna("MISSING")

    # =========================
    # Construção do modelo
    # =========================
    model = MODEL_REGISTRY["catboost"](RANDOM_SEED)

    # =========================
    # Treinamento
    # =========================
    model.fit(
        X_train,
        y_train,
        cat_features=categorical_features,
        eval_set=(X_val, y_val),
        early_stopping_rounds=50,
        verbose=False,
    )

    # =========================
    # Avaliação
    # =========================
    preds = model.predict(X_val)

    rmse = mean_squared_error(y_val, preds) ** 0.5
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)

    logger.info(f"CatBoost V2 (sem id) RMSE (val): {rmse:.4f}")
    logger.info(f"CatBoost V2 (sem id) MAE  (val): {mae:.4f}")
    logger.info(f"CatBoost V2 (sem id) R²   (val): {r2:.4f}")

    # =========================
    # Persistência
    # =========================
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / f"{model_name}.joblib"
    joblib.dump(model, model_path)

    logger.info(f"Modelo salvo em: {model_path.resolve()}")

    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }


if __name__ == "__main__":
    train_catboost_v2_no_id()
