import numpy as np
import joblib
import pandas as pd
from catboost import CatBoostRegressor


def calculate_prediction_interval_hybrid():

    print("🔎 Intervalo Preditivo - Hybrid")

    # 🔹 Carregar modelos
    mincer_model = joblib.load("models/mincer_hybrid_v1.pkl")
    smearing = joblib.load("models/smearing_hybrid_v1.pkl")

    cat_model = CatBoostRegressor()
    cat_model.load_model("models/catboost_residual_v1.cbm")

    df = pd.read_parquet("data/processed/v3/test.parquet")

    target = "renda_mensal_ocupacao_principal_deflacionado"

    X = df.drop(columns=[target]).copy()
    y_log = np.log(df[target])

    # 🔹 IMPORTANTE: usar exatamente as features do residual
    if hasattr(cat_model, "feature_names_"):
        X = X[cat_model.feature_names_]

    # 🔹 Identificar categóricas
    cat_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

    # 🔹 Corrigir categóricas
    for col in cat_features:
        X[col] = (
            X[col]
            .astype(str)
            .replace("nan", "missing")
            .fillna("missing")
        )

    # 🔹 Corrigir numéricas
    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    for col in numeric_cols:
        X[col] = X[col].fillna(X[col].median())

    # 🔹 Predição híbrida
    y_mincer = mincer_model.predict(X)
    residual_pred = cat_model.predict(X)

    y_pred_log = y_mincer + residual_pred

    # 🔹 Intervalo
    residuals = y_log - y_pred_log
    sigma = np.std(residuals)

    print(f"\n📌 Sigma (log): {sigma:.4f}")

    lower_log = y_pred_log - 1.96 * sigma
    upper_log = y_pred_log + 1.96 * sigma

    lower = np.exp(lower_log) * smearing
    upper = np.exp(upper_log) * smearing
    point = np.exp(y_pred_log) * smearing

    print("\n📊 Exemplos:\n")

    for i in range(5):
        print(
            f"Estimativa: {point[i]:.2f} | "
            f"Intervalo: {lower[i]:.2f} - {upper[i]:.2f}"
        )


if __name__ == "__main__":
    calculate_prediction_interval_hybrid()