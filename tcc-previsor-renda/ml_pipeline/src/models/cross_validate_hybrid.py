import numpy as np
import pandas as pd
import joblib
from catboost import CatBoostRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score
from ml_pipeline.src.utils.io import read_parquet
from pathlib import Path


def cross_validate_hybrid():

    print("🔁 Executando 5-Fold Cross Validation (Hybrid V1)")

    df = read_parquet(Path("data/processed/v3/train.parquet"))

    target = "renda_mensal_ocupacao_principal_deflacionado"

    X = df.drop(columns=[target]).copy()
    y_log = np.log(df[target])

    cat_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # tratar categóricas
    for col in cat_features:
        X[col] = X[col].astype(str).fillna("missing")

    # tratar numéricas
    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    for col in numeric_cols:
        X[col] = X[col].fillna(X[col].median())

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    scores = []
    fold = 1

    for train_idx, val_idx in kf.split(X):

        print(f"\n🔹 Fold {fold}")

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y_log.iloc[train_idx], y_log.iloc[val_idx]

        # 1️⃣ Mincer
        from sklearn.linear_model import LinearRegression
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer

        mincer_numeric = ["anos_estudo", "experiencia_aprox", "idade_quadrado"]
        mincer_categorical = ["sexo", "regiao", "possui_carteira_assinada"]

        numeric_pipeline = Pipeline(
            steps=[("imputer", SimpleImputer(strategy="median"))]
        )

        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_pipeline, mincer_numeric),
                ("cat", categorical_pipeline, mincer_categorical),
            ]
        )

        mincer_model = Pipeline(
            steps=[("preprocess", preprocessor), ("regressor", LinearRegression())]
        )

        mincer_model.fit(X_train, y_train)

        y_train_mincer = mincer_model.predict(X_train)
        y_val_mincer = mincer_model.predict(X_val)

        # 2️⃣ Resíduo
        residual_train = y_train - y_train_mincer

        cat_model = CatBoostRegressor(
            iterations=1000,
            depth=8,
            learning_rate=0.05,
            loss_function="RMSE",
            verbose=False,
            random_seed=42
        )

        cat_model.fit(
            X_train,
            residual_train,
            cat_features=cat_features
        )

        residual_pred = cat_model.predict(X_val)

        y_pred_log = y_val_mincer + residual_pred

        r2 = r2_score(y_val, y_pred_log)

        scores.append(r2)

        print(f"R² log Fold {fold}: {r2:.4f}")

        fold += 1

    print("\n📊 RESULTADO FINAL CV (Hybrid)")
    print(f"Média R² log: {np.mean(scores):.4f}")
    print(f"Desvio padrão: {np.std(scores):.4f}")


if __name__ == "__main__":
    cross_validate_hybrid()