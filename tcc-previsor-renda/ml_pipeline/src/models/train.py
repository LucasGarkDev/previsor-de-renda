import joblib
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import (
    TARGET_COLUMN,
    RANDOM_SEED,
    DATA_PROCESSED_DIR,
)

# 🔌 Factory de modelos
from ml_pipeline.src.models.modelsList import MODEL_REGISTRY

logger = get_logger(__name__)


def train(model_name: str = "hist_gb"):
    logger.info(f"Iniciando treino do modelo: {model_name}")

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
    # Tipos de variáveis
    # =========================
    categorical_features = X_train.select_dtypes(include=["object"]).columns.tolist()
    numerical_features = X_train.select_dtypes(exclude=["object"]).columns.tolist()

    logger.info(f"Features numéricas: {numerical_features}")
    logger.info(f"Features categóricas: {categorical_features}")

    # =========================
    # Pré-processamento
    # =========================
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numerical_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )

    # =========================
    # Construção do modelo (factory)
    # =========================
    regressor = MODEL_REGISTRY[model_name](RANDOM_SEED)

    model = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("regressor", regressor),
        ]
    )

    # =========================
    # Treino
    # =========================
    model.fit(X_train, y_train)

    # =========================
    # Avaliação
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

    model_path = models_dir / f"{model_name}.joblib"
    joblib.dump(model, model_path)

    logger.info(f"Modelo salvo em: {model_path.resolve()}")


if __name__ == "__main__":
    train("hist_gb")

