import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.config.settings import DATA_PROCESSED_DIR, TARGET_COLUMN
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def evaluate_model_catboost(model_path):
    logger.info("Iniciando avaliação do CatBoost no conjunto de teste")

    model = joblib.load(model_path)

    test_df = read_parquet(DATA_PROCESSED_DIR / "test.parquet")

    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]

    # 🔴 Remover leakage (consistência com treino)
    leakage_cols = [c for c in X_test.columns if c.startswith("log_")]
    if leakage_cols:
        X_test = X_test.drop(columns=leakage_cols)

    # 🔧 OBRIGATÓRIO: tratar missing em categóricas
    categorical_features = X_test.select_dtypes(include=["object"]).columns.tolist()
    for col in categorical_features:
        X_test[col] = X_test[col].fillna("MISSING")

    preds = model.predict(X_test)

    rmse = mean_squared_error(y_test, preds) ** 0.5
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    metrics = {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }

    logger.info(f"CatBoost RMSE (teste): {rmse:.4f}")
    logger.info(f"CatBoost MAE  (teste): {mae:.4f}")
    logger.info(f"CatBoost R²   (teste): {r2:.4f}")

    return metrics
