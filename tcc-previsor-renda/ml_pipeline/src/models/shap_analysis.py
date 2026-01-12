# ml_pipeline/src/models/shap_analysis.py
# ml_pipeline/src/models/shap_analysis.py
import joblib
import shap
import pandas as pd
from pathlib import Path

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
)

logger = get_logger(__name__)


def run_shap_analysis(model_path: Path, max_rows: int = 300):
    logger.info("Iniciando análise SHAP")

    # =========================
    # Load model and raw data
    # =========================
    pipeline = joblib.load(model_path)
    df = read_parquet(DATA_PROCESSED_DIR / "train.parquet")

    X = df.drop(columns=[TARGET_COLUMN])

    # Remover leakage (mesma regra do treino)
    leakage_cols = [c for c in X.columns if c.startswith("log_")]
    if leakage_cols:
        logger.warning(f"Removendo colunas com vazamento de alvo: {leakage_cols}")
        X = X.drop(columns=leakage_cols)

    # =========================
    # Separate pipeline parts
    # =========================
    preprocessor = pipeline.named_steps["preprocessing"]
    regressor = pipeline.named_steps["regressor"]

    # =========================
    # Transform to numeric matrix
    # =========================
    X_transformed = preprocessor.transform(X)
    feature_names = preprocessor.get_feature_names_out()

    X_transformed_df = pd.DataFrame(
        X_transformed,
        columns=feature_names,
        index=X.index,
    )

    logger.info("Dados transformados para SHAP (matriz numérica)")

    # =========================
    # Sample for performance
    # =========================
    n = min(max_rows, len(X_transformed_df))
    background_df = X_transformed_df.sample(n=n, random_state=42)
    background = background_df.to_numpy()

    logger.warning(
        "XGBoost/Pipeline detectado — usando SHAP model-agnostic (Permutation) "
        "sobre dados pré-processados + regressor.predict"
    )

    # =========================
    # SHAP: model-agnostic on regressor
    # =========================
    masker = shap.maskers.Independent(background)

    explainer = shap.Explainer(
        regressor.predict,     # <- regressor recebe matriz numérica
        masker,
        algorithm="permutation",
    )

    shap_values = explainer(background)

    # =========================
    # Plot
    # =========================
    shap.summary_plot(
        shap_values,
        background_df,
        show=True,
    )

    logger.info("SHAP concluído com sucesso")
