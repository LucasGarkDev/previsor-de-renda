# ml_pipeline/src/models/evaluate_mincer_v1.py

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def add_mincer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["experiencia"] = df["idade"] - df["anos_estudo"] - 6
    df["experiencia"] = df["experiencia"].clip(lower=0)
    df["experiencia_squared"] = df["experiencia"] ** 2

    return df


def evaluate_mincer_v1(
    model_path: str,
    smearing_path: str,
    test_path: str,
):
    print("🟢 Avaliando Modelo Mincer V1...")

    model = joblib.load(model_path)
    smearing_factor = joblib.load(smearing_path)

    df = pd.read_parquet(test_path)

    # Remover renda <= 0
    df = df[df["renda_mensal_ocupacao_principal_deflacionado"] > 0]

    required_cols = [
        "anos_estudo",
        "idade",
        "sexo",
        "possui_carteira_assinada",
        "regiao",
        "renda_mensal_ocupacao_principal_deflacionado",
    ]

    df = df[required_cols].dropna()

    df["anos_estudo"] = df["anos_estudo"].astype(float)
    df["idade"] = df["idade"].astype(float)

    df = add_mincer_features(df)

    feature_cols = [
        "anos_estudo",
        "experiencia",
        "experiencia_squared",
        "sexo",
        "possui_carteira_assinada",
        "regiao",
    ]

    X = df[feature_cols]

    y_true = df["renda_mensal_ocupacao_principal_deflacionado"]
    y_log_true = np.log(y_true)

    # Predição log
    y_pred_log = model.predict(X)

    # Métricas log
    r2_log = r2_score(y_log_true, y_pred_log)
    rmse_log = np.sqrt(mean_squared_error(y_log_true, y_pred_log))
    mae_log = mean_absolute_error(y_log_true, y_pred_log)

    # Retransformação com smearing
    y_pred = np.exp(y_pred_log) * smearing_factor

    # Métricas escala original
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)

    print("\n📊 MÉTRICAS (LOG)")
    print(f"R² log: {r2_log:.4f}")
    print(f"RMSE log: {rmse_log:.4f}")
    print(f"MAE log: {mae_log:.4f}")

    print("\n📊 MÉTRICAS (ESCALA ORIGINAL)")
    print(f"R²: {r2:.4f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")

    # -------------------------
    # Coeficientes (interpretação econômica)
    # -------------------------
    reg = model.named_steps["regressor"]
    feature_names = model.named_steps["preprocess"].get_feature_names_out()

    coef_df = pd.DataFrame({
        "feature": feature_names,
        "coeficiente": reg.coef_
    }).sort_values("coeficiente", ascending=False)

    print("\n📈 Top 10 coeficientes:")
    print(coef_df.head(10))


if __name__ == "__main__":
    evaluate_mincer_v1(
        model_path="artifacts/mincer_v1/model.joblib",
        smearing_path="artifacts/mincer_v1/smearing.joblib",
        test_path="data/processed/v3/test.parquet",
    )