import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score
from ml_pipeline.src.utils.io import read_parquet
from pathlib import Path


def cross_validate_catboost():

    print("🔁 Executando 5-Fold Cross Validation (CatBoost V5)")

    df = read_parquet(Path("data/processed/v3/train.parquet"))

    target = "renda_mensal_ocupacao_principal_deflacionado"

    X = df.drop(columns=[target])
    y = np.log(df[target])

    # 🔹 Identificar categóricas
    cat_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # 🔹 Tratar missing nas categóricas
    for col in cat_features:
        X[col] = X[col].astype(str).fillna("missing")

    # 🔹 Tratar missing nas numéricas
    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    for col in numeric_cols:
        X[col] = X[col].fillna(X[col].median())

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    scores = []

    fold = 1

    for train_idx, val_idx in kf.split(X):

        print(f"\n🔹 Fold {fold}")

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = CatBoostRegressor(
            iterations=1000,
            depth=8,
            learning_rate=0.05,
            loss_function="RMSE",
            verbose=False,
            random_seed=42
        )

        model.fit(
            X_train,
            y_train,
            cat_features=cat_features
        )

        y_pred = model.predict(X_val)

        r2 = r2_score(y_val, y_pred)
        scores.append(r2)

        print(f"R² log Fold {fold}: {r2:.4f}")

        fold += 1

    print("\n📊 RESULTADO FINAL CV")
    print(f"Média R² log: {np.mean(scores):.4f}")
    print(f"Desvio padrão: {np.std(scores):.4f}")


if __name__ == "__main__":
    cross_validate_catboost()