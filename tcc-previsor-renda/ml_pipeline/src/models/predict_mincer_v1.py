# ml_pipeline/src/models/predict_mincer_v1.py

import pandas as pd
import numpy as np
import joblib


def add_mincer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["experiencia"] = df["idade"] - df["anos_estudo"] - 6
    df["experiencia"] = df["experiencia"].clip(lower=0)
    df["experiencia_squared"] = df["experiencia"] ** 2

    return df


def predict_mincer_v1(
    model_path: str,
    smearing_path: str,
    input_df: pd.DataFrame,
) -> pd.DataFrame:

    model = joblib.load(model_path)
    smearing_factor = joblib.load(smearing_path)

    df = add_mincer_features(input_df)

    feature_cols = [
        "anos_estudo",
        "experiencia",
        "experiencia_squared",
        "sexo",
        "possui_carteira_assinada",
        "regiao",
    ]

    X = df[feature_cols]

    y_pred_log = model.predict(X)
    y_pred = np.exp(y_pred_log) * smearing_factor

    df["renda_prevista_mincer"] = y_pred

    return df