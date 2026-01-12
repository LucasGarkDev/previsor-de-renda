# ml_pipeline/src/models/modelsList/xgboost.py

from xgboost import XGBRegressor


def build_model(random_state: int):
    """
    Factory do XGBoost Regressor.
    Retorna APENAS o estimador (sem pipeline).
    """

    return XGBRegressor(
        # =========================
        # Configuração principal
        # =========================
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        min_child_weight=1,
        subsample=0.8,
        colsample_bytree=0.8,

        # =========================
        # Regularização
        # =========================
        reg_alpha=0.0,
        reg_lambda=1.0,

        # =========================
        # Objetivo
        # =========================
        objective="reg:squarederror",

        # =========================
        # Reprodutibilidade
        # =========================
        random_state=random_state,
        n_jobs=-1,
        verbosity=0,
    )

