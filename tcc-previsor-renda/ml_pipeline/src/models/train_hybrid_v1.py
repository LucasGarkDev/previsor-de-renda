# ml_pipeline/src/models/train_hybrid_v1.py

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from catboost import CatBoostRegressor

from ml_pipeline.src.utils.io import read_parquet


def train_hybrid_v1():

    print("🔵 Treinando Modelo Híbrido V1 (Mincer + CatBoost Residual)...")

    # ==========================================================
    # 1️⃣ Carregar dados
    # ==========================================================
    train = read_parquet(Path("data/processed/v3/train.parquet"))
    val   = read_parquet(Path("data/processed/v3/validation.parquet"))

    target = "renda_mensal_ocupacao_principal_deflacionado"

    # ==========================================================
    # 2️⃣ Garantir tipos numéricos corretos
    # ==========================================================
    numeric_cast_cols = [
        "anos_estudo",
        "experiencia_aprox",
        "idade_quadrado",
        target
    ]

    for col in numeric_cast_cols:
        train[col] = pd.to_numeric(train[col], errors="coerce")
        val[col]   = pd.to_numeric(val[col], errors="coerce")

    # ==========================================================
    # 3️⃣ Target em log
    # ==========================================================
    y_train_log = np.log(train[target])
    y_val_log   = np.log(val[target])

    # ==========================================================
    # 4️⃣ Mincer (Modelo Estrutural)
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

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median"))
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, mincer_numeric),
            ("cat", categorical_pipeline, mincer_categorical)
        ]
    )

    mincer_model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("regressor", LinearRegression())
        ]
    )

    # Usar apenas colunas necessárias
    X_train_mincer = train[mincer_numeric + mincer_categorical]
    X_val_mincer   = val[mincer_numeric + mincer_categorical]

    mincer_model.fit(X_train_mincer, y_train_log)

    y_train_mincer = mincer_model.predict(X_train_mincer)
    y_val_mincer   = mincer_model.predict(X_val_mincer)

    # ==========================================================
    # 5️⃣ Resíduos (no log)
    # ==========================================================
    residual_train = y_train_log - y_train_mincer
    residual_val   = y_val_log   - y_val_mincer

    # ==========================================================
    # 6️⃣ Features completas para CatBoost
    # ==========================================================
    drop_cols = [target, "id_domicilio"]

    X_train_cat = train.drop(columns=drop_cols).copy()
    X_val_cat   = val.drop(columns=drop_cols).copy()

    # Identificar categóricas automaticamente
    cat_features = X_train_cat.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # ==========================================================
    # 🔥 LIMPEZA DEFINITIVA PARA CATBOOST
    # ==========================================================

    for col in cat_features:
        X_train_cat[col] = (
            X_train_cat[col]
            .astype(str)
            .fillna("MISSING")
        )

        X_val_cat[col] = (
            X_val_cat[col]
            .astype(str)
            .fillna("MISSING")
        )

    # ==========================================================
    # 7️⃣ Treinar CatBoost nos resíduos
    # ==========================================================
    cat_model = CatBoostRegressor(
        iterations=1000,
        depth=8,
        learning_rate=0.05,
        loss_function="RMSE",
        random_seed=42,
        verbose=100
    )

    cat_model.fit(
        X_train_cat,
        residual_train,
        eval_set=(X_val_cat, residual_val),
        cat_features=cat_features,
        early_stopping_rounds=100
    )

    # ==========================================================
    # 8️⃣ Smearing Factor
    # ==========================================================
    smearing_factor = np.mean(np.exp(residual_train))

    print(f"📌 Smearing factor (Hybrid): {smearing_factor:.6f}")

    # ==========================================================
    # 9️⃣ Salvar modelos
    # ==========================================================
    Path("models").mkdir(exist_ok=True)

    joblib.dump(mincer_model, "models/mincer_hybrid_v1.pkl")
    cat_model.save_model("models/catboost_residual_v1.cbm")
    joblib.dump(smearing_factor, "models/smearing_hybrid_v1.pkl")

    print("✅ Modelo Híbrido treinado com sucesso.")


if __name__ == "__main__":
    train_hybrid_v1()