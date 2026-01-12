# ml_pipeline/src/models/modelsList/hist_gradient_boosting.py

from sklearn.ensemble import HistGradientBoostingRegressor


def build_model(random_state: int):
    return HistGradientBoostingRegressor(
        max_depth=8,
        learning_rate=0.05,
        max_iter=300,
        random_state=random_state,
    )
