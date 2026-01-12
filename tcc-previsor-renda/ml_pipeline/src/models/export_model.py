# ml_pipeline/src/models/export_model.py
import joblib
import json
from pathlib import Path

from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import PROJECT_ROOT, TARGET_COLUMN

logger = get_logger(__name__)


def export_model(model_path, model_name, metrics):
    export_dir = PROJECT_ROOT / "exported_models" / model_name
    export_dir.mkdir(parents=True, exist_ok=True)

    exported_model_path = export_dir / f"{model_name}.joblib"
    joblib.dump(joblib.load(model_path), exported_model_path)

    metadata = {
        "model_name": model_name,
        "target": TARGET_COLUMN,
        "metrics": metrics,
        "status": "validado",
    }

    with open(export_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Modelo exportado para {export_dir.resolve()}")
