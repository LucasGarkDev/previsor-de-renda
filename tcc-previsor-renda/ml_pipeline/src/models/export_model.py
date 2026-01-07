import joblib
import json
from pathlib import Path

from ml_pipeline.src.config.settings import PROJECT_ROOT
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def export_model():
    logger.info("Exportando modelo e metadados")

    models_dir = PROJECT_ROOT / "models"
    model_path = models_dir / "baseline_elasticnet.joblib"
    export_dir = PROJECT_ROOT / "exported_models"

    export_dir.mkdir(exist_ok=True)

    # Copiar modelo
    exported_model_path = export_dir / "baseline_elasticnet.joblib"
    joblib.dump(joblib.load(model_path), exported_model_path)

    # Metadados
    metadata = {
        "model": "ElasticNet",
        "type": "baseline",
        "target": "renda_mensal_ocupacao_principal_deflacionado",
        "status": "validado",
    }

    with open(export_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Modelo exportado para {export_dir.resolve()}")


if __name__ == "__main__":
    export_model()
