import joblib
import shap
import pandas as pd
from pathlib import Path

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    PROJECT_ROOT,
)

logger = get_logger(__name__)


def run_shap_analysis():
    logger.info("Iniciando análise SHAP")

    # =========================
    # Paths
    # =========================
    model_path = PROJECT_ROOT / "models" / "baseline_elasticnet.joblib"
    data_path = DATA_PROCESSED_DIR / "train.parquet"

    # =========================
    # Load model and data
    # =========================
    pipeline = joblib.load(model_path)
    df = read_parquet(data_path)

    X = df.drop(columns=[TARGET_COLUMN])

    # =========================
    # Separar pipeline
    # =========================
    preprocessor = pipeline.named_steps["preprocessing"]
    regressor = pipeline.named_steps["regressor"]

    # =========================
    # Transformar X
    # =========================
    X_transformed = preprocessor.transform(X)

    # Nomes das features após OneHot
    feature_names = preprocessor.get_feature_names_out()
    X_transformed_df = pd.DataFrame(
        X_transformed,
        columns=feature_names,
        index=X.index,
    )

    logger.info("Dados transformados para SHAP")

    # =========================
    # SHAP Explainer
    # =========================
    explainer = shap.Explainer(regressor, X_transformed_df)
    shap_values = explainer(X_transformed_df)

    # =========================
    # Plots
    # =========================
    shap.summary_plot(shap_values, X_transformed_df)


if __name__ == "__main__":
    run_shap_analysis()
