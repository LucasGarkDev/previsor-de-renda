from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
from catboost import CatBoostRegressor
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parents[3]
MINCER_MODEL_PATH = BASE_DIR / "models" / "mincer_hybrid_v1.pkl"
CATBOOST_RESIDUAL_PATH = BASE_DIR / "models" / "catboost_residual_v1.cbm"
SMEARING_PATH = BASE_DIR / "models" / "smearing_hybrid_v1.pkl"


@dataclass(frozen=True)
class HybridModelBundle:
    mincer_model: Pipeline
    residual_model: CatBoostRegressor
    smearing_factor: float


class ModelLoader:
    _bundle: HybridModelBundle | None = None

    @classmethod
    def get_bundle(cls) -> HybridModelBundle:
        if cls._bundle is None:
            cls._bundle = cls._load_bundle()
        return cls._bundle

    @staticmethod
    def _load_bundle() -> HybridModelBundle:
        for path in (MINCER_MODEL_PATH, CATBOOST_RESIDUAL_PATH, SMEARING_PATH):
            if not path.exists():
                raise FileNotFoundError(f"Artefato do modelo hibrido nao encontrado: {path}")

        mincer_model = joblib.load(MINCER_MODEL_PATH)
        residual_model = CatBoostRegressor()
        residual_model.load_model(CATBOOST_RESIDUAL_PATH)
        smearing_factor = float(joblib.load(SMEARING_PATH))

        return HybridModelBundle(
            mincer_model=mincer_model,
            residual_model=residual_model,
            smearing_factor=smearing_factor,
        )
