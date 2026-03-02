# ml_pipeline/src/models/evaluate_hybrid_v1.py

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from catboost import CatBoostRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from ml_pipeline.src.utils.io import read_parquet


def evaluate_hybrid_v1():

    print("🟢 Avaliando Modelo Híbrido V1...")

    # ==========================================================
    # 1️⃣ Carregar modelos
    # ==========================================================
    mincer_model = joblib.load("models/mincer_hybrid_v1.pkl")

    cat_model = CatBoostRegressor()
    cat_model.load_model("models/catboost_residual_v1.cbm")

    smearing_factor = joblib.load("models/smearing_hybrid_v1.pkl")

    # ==========================================================
    # 2️⃣ Carregar dados
    # ==========================================================
    test = read_parquet(Path("data/processed/v3/test.parquet"))

    target = "renda_mensal_ocupacao_principal_deflacionado"

    # Garantir tipo numérico
    numeric_cast_cols = [
        "anos_estudo",
        "experiencia_aprox",
        "idade_quadrado",
        target
    ]

    for col in numeric_cast_cols:
        test[col] = pd.to_numeric(test[col], errors="coerce")

    # ==========================================================
    # 3️⃣ Target
    # ==========================================================
    y_true = test[target]
    y_log_true = np.log(y_true)

    # ==========================================================
    # 4️⃣ Parte Mincer
    # ==========================================================
    mincer_numeric = [
        "anos_estudo",
        "experiencia_aprox",
        "idade_quadrado"
    ]

    mincer_categorical = [
        "sexo",
        "regiao",
        "possui_carteira_assinada"
    ]

    X_test_mincer = test[mincer_numeric + mincer_categorical]

    y_mincer_log = mincer_model.predict(X_test_mincer)

    # ==========================================================
    # 5️⃣ Parte CatBoost (resíduos)
    # ==========================================================
    drop_cols = [target, "id_domicilio"]

    X_test_cat = test.drop(columns=drop_cols).copy()

    cat_features = X_test_cat.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # 🔥 LIMPEZA OBRIGATÓRIA (mesma do treino)
    for col in cat_features:
        X_test_cat[col] = (
            X_test_cat[col]
            .astype(str)
            .fillna("MISSING")
        )

    residual_pred = cat_model.predict(X_test_cat)

    # ==========================================================
    # 6️⃣ Combinação híbrida
    # ==========================================================
    y_pred_log = y_mincer_log + residual_pred

    # Reverter log + smearing
    y_pred = np.exp(y_pred_log) * smearing_factor

    # ==========================================================
    # 7️⃣ Métricas
    # ==========================================================
    print("\n📊 MÉTRICAS (LOG)")
    print("R² log:", round(r2_score(y_log_true, y_pred_log), 4))
    print("RMSE log:", round(np.sqrt(mean_squared_error(y_log_true, y_pred_log)), 4))
    print("MAE log:", round(mean_absolute_error(y_log_true, y_pred_log), 4))

    print("\n📊 MÉTRICAS (ESCALA ORIGINAL)")
    print("R²:", round(r2_score(y_true, y_pred), 4))
    print("RMSE:", round(np.sqrt(mean_squared_error(y_true, y_pred)), 2))
    print("MAE:", round(mean_absolute_error(y_true, y_pred), 2))

    print("\n✅ Avaliação concluída.")


if __name__ == "__main__":
    evaluate_hybrid_v1()