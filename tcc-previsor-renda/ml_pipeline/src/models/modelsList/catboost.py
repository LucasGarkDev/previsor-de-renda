from catboost import CatBoostRegressor


def build_model(
    random_state: int,
    depth: int = 8,
    learning_rate: float = 0.05,
    iterations: int = 800,
):
    return CatBoostRegressor(
        iterations=iterations,
        depth=depth,
        learning_rate=learning_rate,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=random_state,
        verbose=False,
    )
