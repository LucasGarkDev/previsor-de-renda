# ml_pipeline/src/models/evaluate.py
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import DATA_PROCESSED_DIR, TARGET_COLUMN

logger = get_logger(__name__)


def evaluate_model(model_path):
    logger.info("Iniciando avaliação no conjunto de teste")

    model = joblib.load(model_path)
    test_df = read_parquet(DATA_PROCESSED_DIR / "test.parquet")

    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]

    preds = model.predict(X_test)

    rmse = mean_squared_error(y_test, preds) ** 0.5
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    metrics = {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }

    logger.info(f"Teste RMSE: {rmse:.4f}")
    logger.info(f"Teste MAE : {mae:.4f}")
    logger.info(f"Teste R²  : {r2:.4f}")

    return metrics
