from catboost import CatBoostRegressor


def build_model(random_state: int):
    """
    Factory do CatBoost Regressor.
    Retorna APENAS o estimador (sem pipeline).
    """

    return CatBoostRegressor(
        iterations=500,
        depth=8,
        learning_rate=0.05,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=random_state,
        verbose=False
    )
