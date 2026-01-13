import joblib
import shap

from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.config.settings import DATA_PROCESSED_DIR
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def run_shap_analysis_catboost(model_path):
    logger.info("Iniciando análise SHAP (CatBoost)")

    # =========================
    # Carregar modelo
    # =========================
    model = joblib.load(model_path)

    # =========================
    # Dados de teste
    # =========================
    test_df = read_parquet(DATA_PROCESSED_DIR / "test.parquet")

    X_test = test_df.drop(columns=["renda_mensal_ocupacao_principal_deflacionado"])

    # ⚠️ Mesma limpeza do treino
    leakage_cols = [c for c in X_test.columns if c.startswith("log_")]
    if leakage_cols:
        X_test = X_test.drop(columns=leakage_cols)

    # Missing categóricos (consistência!)
    categorical_features = X_test.select_dtypes(include=["object"]).columns.tolist()
    for col in categorical_features:
        X_test[col] = X_test[col].fillna("MISSING")

    # =========================
    # SHAP nativo do CatBoost
    # =========================
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # =========================
    # Plot global
    # =========================
    shap.summary_plot(
        shap_values,
        X_test,
        show=True
    )

    logger.info("Análise SHAP (CatBoost) finalizada")
