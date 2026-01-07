import joblib
from pathlib import Path

from sklearn.linear_model import ElasticNet
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

logger = get_logger(__name__)


def train_baseline():
    logger.info("Iniciando treino do modelo baseline (ElasticNet)")

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
    leakage_cols = [col for col in X_train.columns if col.startswith("log_")]
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
    # Pipeline completo
    # =========================
    model = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            (
                "regressor",
                ElasticNet(
                    alpha=1.0,
                    l1_ratio=0.5,
                    random_state=RANDOM_SEED,
                ),
            ),
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

    mse = mean_squared_error(y_val, preds)
    rmse = mse ** 0.5
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)

    logger.info(f"Baseline RMSE (validação): {rmse:.4f}")
    logger.info(f"Baseline MAE  (validação): {mae:.4f}")
    logger.info(f"Baseline R²   (validação): {r2:.4f}")

    # =========================
    # Persistência
    # =========================
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "baseline_elasticnet.joblib"
    joblib.dump(model, model_path)

    logger.info(f"Modelo baseline salvo em: {model_path.resolve()}")


if __name__ == "__main__":
    train_baseline()
