# ml_pipeline/src/models/predict_smearing.py

"""
Utilitário de predição para modelos V4 (Log + Smearing)

Responsável por:
- Carregar bundle salvo
- Aplicar transformação inversa corretamente
- Aplicar smearing factor (se habilitado)
- Garantir alinhamento de features
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Union

from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def load_bundle(model_path: Union[str, Path]):
    """Carrega bundle completo do modelo V4."""
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

    bundle = joblib.load(model_path)

    required_keys = [
        "model",
        "feature_names",
        "cat_features",
        "smearing_factor",
        "use_log1p",
    ]

    for key in required_keys:
        if key not in bundle:
            raise ValueError(f"Bundle inválido. Chave ausente: {key}")

    logger.info(f"Bundle carregado: {model_path.name}")
    return bundle


def _inverse_log(y_log, use_log1p):
    if use_log1p:
        return np.expm1(y_log)
    return np.exp(y_log)


def predict_income(bundle, X):
    """
    Gera predição de renda na escala original.
    """

    model = bundle["model"]
    expected_features = bundle["feature_names"]
    smearing_factor = bundle["smearing_factor"]
    use_log1p = bundle["use_log1p"]

    # =========================
    # Alinhar features
    # =========================
    missing_cols = set(expected_features) - set(X.columns)
    if missing_cols:
        raise ValueError(f"Colunas ausentes para predição: {missing_cols}")

    X_aligned = X[expected_features].copy()

    # =========================
    # Predição no log
    # =========================
    preds_log = model.predict(X_aligned)

    # =========================
    # Voltar para escala real
    # =========================
    preds = _inverse_log(preds_log, use_log1p) * smearing_factor

    return preds