# ml_pipeline/src/models/postprocess.py
from pathlib import Path

from ml_pipeline.src.models.evaluate import evaluate_model
from ml_pipeline.src.models.shap_analysis import run_shap_analysis
from ml_pipeline.src.models.export_model import export_model
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import PROJECT_ROOT

logger = get_logger(__name__)


def run_postprocess(model_name: str):
    logger.info(f"Iniciando pós-processamento do modelo: {model_name}")

    model_path = PROJECT_ROOT / "models" / f"{model_name}.joblib"

    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

    # 1. Avaliação
    metrics = evaluate_model(model_path)

    # 2. SHAP
    run_shap_analysis(model_path)

    # 3. Exportação
    export_model(
        model_path=model_path,
        model_name=model_name,
        metrics=metrics,
    )

    logger.info("Pós-processamento finalizado com sucesso")


if __name__ == "__main__":
    # exemplo:
    run_postprocess("hist_gb")
