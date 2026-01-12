# ml_pipeline/src/models/modelsList/elasticnet.py

from sklearn.linear_model import ElasticNet


def build_model(random_state: int):
    return ElasticNet(
        alpha=1.0,
        l1_ratio=0.5,
        random_state=random_state,
    )
