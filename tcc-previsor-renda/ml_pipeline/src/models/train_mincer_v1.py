# ml_pipeline/src/models/train_mincer_v1.py

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score


# ==========================================
# Feature Engineering — Mincer
# ==========================================

def add_mincer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["experiencia"] = df["idade"] - df["anos_estudo"] - 6
    df["experiencia"] = df["experiencia"].clip(lower=0)
    df["experiencia_squared"] = df["experiencia"] ** 2

    return df


# ==========================================
# Treinamento
# ==========================================

def train_mincer_v1(
    train_path: str,
    model_output_path: str,
    smearing_output_path: str,
):
    print("🔵 Treinando Modelo Mincer V1...")

    df = pd.read_parquet(train_path)

    # Remover renda <= 0 para evitar log inválido
    df = df[df["renda_mensal_ocupacao_principal_deflacionado"] > 0]

    # Selecionar apenas colunas necessárias
    required_cols = [
        "anos_estudo",
        "idade",
        "sexo",
        "possui_carteira_assinada",
        "regiao",
        "renda_mensal_ocupacao_principal_deflacionado",
    ]

    df = df[required_cols].dropna()

    # Converter tipos numéricos se necessário
    df["anos_estudo"] = df["anos_estudo"].astype(float)
    df["idade"] = df["idade"].astype(float)

    df = add_mincer_features(df)

    # Target log-transformado
    y = np.log(df["renda_mensal_ocupacao_principal_deflacionado"])

    feature_cols = [
        "anos_estudo",
        "experiencia",
        "experiencia_squared",
        "sexo",
        "possui_carteira_assinada",
        "regiao",
    ]

    X = df[feature_cols]

    categorical_features = [
        "sexo",
        "possui_carteira_assinada",
        "regiao",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ],
        remainder="passthrough",
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("regressor", LinearRegression()),
        ]
    )

    model.fit(X, y)

    # -------------------------
    # Smearing correction
    # -------------------------
    y_pred_log = model.predict(X)
    residuals = y - y_pred_log
    smearing_factor = np.mean(np.exp(residuals))

    print(f"📌 Smearing factor: {smearing_factor:.6f}")

    # -------------------------
    # Salvar artefatos
    # -------------------------
    Path(model_output_path).parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_output_path)
    joblib.dump(smearing_factor, smearing_output_path)

    r2 = r2_score(y, y_pred_log)

    print("✅ Modelo Mincer treinado com sucesso.")
    print(f"📊 R² (log treino): {r2:.4f}")


if __name__ == "__main__":
    train_mincer_v1(
        train_path="data/processed/v3/train.parquet",
        model_output_path="artifacts/mincer_v1/model.joblib",
        smearing_output_path="artifacts/mincer_v1/smearing.joblib",
    )