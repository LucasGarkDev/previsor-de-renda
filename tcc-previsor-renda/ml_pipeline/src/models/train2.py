import joblib
from pathlib import Path

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import (
    TARGET_COLUMN,
    RANDOM_SEED,
    DATA_PROCESSED_DIR,
)

# Factory
from ml_pipeline.src.models.modelsList import MODEL_REGISTRY

logger = get_logger(__name__)


def train_catboost(
    depth: int = 8,
    learning_rate: float = 0.05,
    iterations: int = 800,
    save_suffix: str | None = None,
):
    model_name = "catboost"
    logger.info(
        f"Iniciando treino do modelo: {model_name} | "
        f"depth={depth} | lr={learning_rate} | iterations={iterations}"
    )

    if model_name not in MODEL_REGISTRY:
        raise ValueError(
            f"Modelo '{model_name}' não registrado. "
            f"Disponíveis: {list(MODEL_REGISTRY.keys())}"
        )

    # =========================
    # Leitura dos dados
    # =========================
    train_df = read_parquet(DATA_PROCESSED_DIR / "train.parquet")
    val_df = read_parquet(DATA_PROCESSED_DIR / "validation.parquet")

    # =========================
    # Separação X / y
    # =========================
    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_val = val_df.drop(columns=[TARGET_COLUMN])
    y_val = val_df[TARGET_COLUMN]

    # =========================
    # REMOVER LEAKAGE (CRÍTICO)
    # =========================
    leakage_cols = [c for c in X_train.columns if c.startswith("log_")]
    if leakage_cols:
        logger.warning(f"Removendo colunas com vazamento de alvo: {leakage_cols}")
        X_train = X_train.drop(columns=leakage_cols)
        X_val = X_val.drop(columns=leakage_cols)

    # =========================
    # Identificação de categóricas
    # =========================
    categorical_features = X_train.select_dtypes(include=["object"]).columns.tolist()

    logger.info(f"Features categóricas (CatBoost): {categorical_features}")
    logger.info(f"Total de features: {X_train.shape[1]}")

    # =========================
    # Tratamento de missing em categóricas (OBRIGATÓRIO p/ CatBoost)
    # =========================
    for col in categorical_features:
        X_train[col] = X_train[col].fillna("MISSING")
        X_val[col] = X_val[col].fillna("MISSING")

    # =========================
    # Construção do modelo (parametrizada)
    # =========================
    model = MODEL_REGISTRY[model_name](
        RANDOM_SEED,
        depth=depth,
        learning_rate=learning_rate,
        iterations=iterations,
    )

    # =========================
    # Treinamento
    # =========================
    model.fit(
        X_train,
        y_train,
        cat_features=categorical_features,
        eval_set=(X_val, y_val),
        early_stopping_rounds=50,
    )

    # =========================
    # Avaliação (validação)
    # =========================
    preds = model.predict(X_val)

    rmse = mean_squared_error(y_val, preds) ** 0.5
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)

    logger.info(f"{model_name} RMSE (validação): {rmse:.4f}")
    logger.info(f"{model_name} MAE  (validação): {mae:.4f}")
    logger.info(f"{model_name} R²   (validação): {r2:.4f}")

    # =========================
    # Persistência
    # =========================
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    suffix = f"_{save_suffix}" if save_suffix else ""
    model_path = models_dir / f"{model_name}{suffix}.joblib"
    joblib.dump(model, model_path)

    logger.info(f"Modelo salvo em: {model_path.resolve()}")

    # =========================
    # Retorno das métricas (IMPORTANTE p/ tuning)
    # =========================
    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }


if __name__ == "__main__":
    train_catboost()
