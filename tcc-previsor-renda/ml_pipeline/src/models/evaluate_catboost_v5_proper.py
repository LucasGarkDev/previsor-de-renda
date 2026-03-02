import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def evaluate_catboost(path):

    print(f"\n🔎 Avaliando {path}")
    
    obj = joblib.load(path)
    
    model = obj["model"]
    smearing = obj["smearing_factor"]
    cat_features = obj["cat_features"]

    df = pd.read_parquet("data/processed/v3/test.parquet")

    target = "renda_mensal_ocupacao_principal_deflacionado"

    y = df[target]
    y_log = np.log(y)

    # ===============================
    # 🔎 Garantir mesma estrutura do treino
    # ===============================

    expected_features = model.feature_names_
    print("\nFeatures esperadas pelo modelo:")
    print(expected_features)

    # Selecionar exatamente as features usadas no treino
    X = df[expected_features].copy()

    # Converter categóricas corretamente
    for col in cat_features:
        if col in X.columns:
            X[col] = X[col].astype(str)

    # ===============================
    # 📈 Predição
    # ===============================

    y_pred_log = model.predict(X)
    y_pred = np.exp(y_pred_log) * smearing

    # ===============================
    # 📊 Métricas
    # ===============================

    print("\n📊 MÉTRICAS (LOG)")
    print("R² log:", round(r2_score(y_log, y_pred_log), 4))
    print("RMSE log:", round(np.sqrt(mean_squared_error(y_log, y_pred_log)), 4))
    print("MAE log:", round(mean_absolute_error(y_log, y_pred_log), 4))

    print("\n📊 MÉTRICAS (ESCALA ORIGINAL)")
    print("R²:", round(r2_score(y, y_pred), 4))
    print("RMSE:", round(np.sqrt(mean_squared_error(y, y_pred)), 2))
    print("MAE:", round(mean_absolute_error(y, y_pred), 2))


if __name__ == "__main__":
    evaluate_catboost("models/catboost_v5_global.joblib")