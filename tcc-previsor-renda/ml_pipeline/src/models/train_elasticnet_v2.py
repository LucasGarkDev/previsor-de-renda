# ml_pipeline/src/models/train_elasticnet_v2.py

"""
Treinamento do modelo ElasticNet — versão v2
(Baseline contextual com variáveis domiciliares)
"""

import joblib
from pathlib import Path

from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    RANDOM_SEED,
)

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def train_elasticnet_v2():
    logger.info("Iniciando treino do ElasticNet V2 (baseline contextual)")

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
    # Separação de tipos
    # =========================
    numeric_features = X_train.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X_train.select_dtypes(include=["object", "category"]).columns.tolist()

    logger.info(f"Numéricas ({len(numeric_features)}): {numeric_features}")
    logger.info(f"Categóricas ({len(categorical_features)}): {categorical_features}")

    # =========================
    # Pré-processamento correto
    # =========================
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            (
                "cat",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                categorical_features,
            ),
        ]
    )

    model = ElasticNet(
        alpha=1.0,
        l1_ratio=0.5,
        random_state=RANDOM_SEED,
        max_iter=5000,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )

    # =========================
    # Treinamento
    # =========================
    pipeline.fit(X_train, y_train)

    # =========================
    # Avaliação
    # =========================
    preds = pipeline.predict(X_val)

    rmse = mean_squared_error(y_val, preds) ** 0.5
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)

    logger.info(f"ElasticNet V2 RMSE (val): {rmse:.4f}")
    logger.info(f"ElasticNet V2 MAE  (val): {mae:.4f}")
    logger.info(f"ElasticNet V2 R²   (val): {r2:.4f}")

    # =========================
    # Salvamento
    # =========================
    output_dir = Path("models")
    output_dir.mkdir(exist_ok=True)

    model_path = output_dir / "elasticnet_v2.joblib"
    joblib.dump(pipeline, model_path)

    logger.info(f"Modelo ElasticNet V2 salvo em: {model_path.resolve()}")

    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }


if __name__ == "__main__":
    train_elasticnet_v2()
