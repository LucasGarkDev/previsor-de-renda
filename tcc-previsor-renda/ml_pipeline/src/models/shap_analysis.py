# ml_pipeline/src/models/shap_analysis.py
import joblib
import shap
import pandas as pd

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import DATA_PROCESSED_DIR, TARGET_COLUMN

logger = get_logger(__name__)


def run_shap_analysis(model_path, max_samples=2000):
    logger.info("Iniciando análise SHAP")

    pipeline = joblib.load(model_path)
    df = read_parquet(DATA_PROCESSED_DIR / "train.parquet")

    if len(df) > max_samples:
        df = df.sample(max_samples, random_state=42)

    X = df.drop(columns=[TARGET_COLUMN])

    preprocessor = pipeline.named_steps["preprocessing"]
    regressor = pipeline.named_steps["regressor"]

    X_transformed = preprocessor.transform(X)
    feature_names = preprocessor.get_feature_names_out()

    X_transformed_df = pd.DataFrame(
        X_transformed,
        columns=feature_names,
        index=X.index,
    )

    explainer = shap.Explainer(regressor, X_transformed_df)
    shap_values = explainer(X_transformed_df)

    shap.summary_plot(shap_values, X_transformed_df)

    logger.info("SHAP concluído")
