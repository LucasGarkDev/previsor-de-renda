import numpy as np
import joblib
import pandas as pd


def calculate_prediction_interval():

    print("🔎 Calculando Intervalo Preditivo")

    obj = joblib.load("models/catboost_v5_global.joblib")

    model = obj["model"]
    smearing = obj["smearing_factor"]
    cat_features = obj["cat_features"]

    df = pd.read_parquet("data/processed/v3/test.parquet")

    target = "renda_mensal_ocupacao_principal_deflacionado"

    X = df.drop(columns=[target]).copy()
    y = df[target]
    y_log = np.log(y)

    # 🔹 Garantir mesmas colunas usadas no treino
    if hasattr(model, "feature_names_"):
        X = X[model.feature_names_]

    # 🔹 Corrigir categóricas
    for col in cat_features:
        if col in X.columns:
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

    # 🔹 Previsão
    y_pred_log = model.predict(X)

    residuals = y_log - y_pred_log

    sigma = np.std(residuals)

    print(f"\n📌 Desvio padrão dos resíduos (log): {sigma:.4f}")

    # Intervalo 95%
    lower_log = y_pred_log - 1.96 * sigma
    upper_log = y_pred_log + 1.96 * sigma

    lower = np.exp(lower_log) * smearing
    upper = np.exp(upper_log) * smearing
    point = np.exp(y_pred_log) * smearing

    print("\n📊 Exemplo de intervalo para primeiras 5 previsões:\n")

    for i in range(5):
        print(
            f"Estimativa: {point[i]:.2f} | "
            f"Intervalo: {lower[i]:.2f} - {upper[i]:.2f}"
        )


if __name__ == "__main__":
    calculate_prediction_interval()