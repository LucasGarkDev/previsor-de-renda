# ml_pipeline/src/models/postprocess2.py
from pathlib import Path

from ml_pipeline.src.models.evaluate_model_catboost import evaluate_model_catboost
from ml_pipeline.src.models.export_model import export_model
from ml_pipeline.src.models.shap_analysis_catboost import run_shap_analysis_catboost
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import PROJECT_ROOT

logger = get_logger(__name__)


def run_postprocess_catboost():
    model_name = "catboost"
    logger.info(f"Iniciando pós-processamento do modelo: {model_name}")

    model_path = PROJECT_ROOT / "models" / f"{model_name}.joblib"

    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

    # =========================
    # 1. Avaliação
    # =========================
    metrics = evaluate_model_catboost(model_path)

    # =========================
    # 2. SHAP (CatBoost nativo)
    # =========================
    run_shap_analysis_catboost(model_path)

    # =========================
    # 3. Exportação
    # =========================
    export_model(
        model_path=model_path,
        model_name=model_name,
        metrics=metrics,
    )

    logger.info("Pós-processamento do CatBoost finalizado com sucesso")


if __name__ == "__main__":
    run_postprocess_catboost()
