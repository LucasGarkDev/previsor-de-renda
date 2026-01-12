# ml_pipeline/src/models/modelsList/__init__.py
from ml_pipeline.src.models.modelsList.elasticnet import build_model as elasticnet
from ml_pipeline.src.models.modelsList.hist_gradient_boosting import build_model as hist_gb
from ml_pipeline.src.models.modelsList.xgboost import build_model as xgboost

MODEL_REGISTRY = {
    "elasticnet": elasticnet,
    "hist_gb": hist_gb,
    "xgboost": xgboost,
}

