"""
Treinamento CatBoost V8 — Multi-Ano (2015–2024)
Split temporal realista
"""

import numpy as np
import pandas as pd
from google.cloud import bigquery
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from pathlib import Path
import joblib

from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.settings import RANDOM_SEED

logger = get_logger(__name__)

PROJECT_ID = "seu_project_id"  # ajuste
USE_LOG1P = True
ENABLE_SMEARING = True


# ======================================================
# Transformações
# ======================================================

def log_transform(y):
    return np.log1p(y) if USE_LOG1P else np.log(y)


def inverse_log(y_log):
    return np.expm1(y_log) if USE_LOG1P else np.exp(y_log)


# ======================================================
# Query BigQuery
# ======================================================

def fetch_multi_year_data():

    logger.info("Buscando dados multi-ano no BigQuery...")

    client = bigquery.Client(project=PROJECT_ID)

    query = """
    SELECT
      ano,
      trimestre,
      sigla_uf,
      sexo,
      raca_cor,
      idade,
      anos_estudo,
      sabe_ler_escrever,
      trabalhou_semana,
      horas_trabalhadas_semana,
      posicao_ocupacao,
      possui_carteira_assinada,
      zona_urbana,
      regiao,
      atividade_ramo_negocio_semana,
      ocupacao_semana,
      renda_mensal_ocupacao_principal_deflacionado,

      -- V8 Features
      ano - 2015 AS ano_normalizado,
      IF(ano IN (2020, 2021), 1, 0) AS dummy_pandemia,
      ano + (trimestre - 1) / 4.0 AS tempo_continuo

    FROM
      `basedosdados.br_ibge_pnadc.microdados`
    WHERE
      ano BETWEEN 2015 AND 2024
      AND renda_mensal_ocupacao_principal_deflacionado IS NOT NULL
    """

    df = client.query(query).to_dataframe()

    logger.info(f"Total registros carregados: {len(df)}")

    return df


# ======================================================
# Split Temporal
# ======================================================

def temporal_split(df):

    train_df = df[df["ano"] <= 2022]
    val_df = df[df["ano"] == 2023]
    test_df = df[df["ano"] == 2024]

    logger.info(f"Train: {len(train_df)}")
    logger.info(f"Validation: {len(val_df)}")
    logger.info(f"Test: {len(test_df)}")

    return train_df, val_df, test_df


# ======================================================
# Treino
# ======================================================

def train_v8():

    logger.info("Iniciando V8 Multi-Ano")

    df = fetch_multi_year_data()

    train_df, val_df, test_df = temporal_split(df)

    TARGET = "renda_mensal_ocupacao_principal_deflacionado"

    y_train_raw = train_df[TARGET]
    y_val_raw = val_df[TARGET]
    y_test_raw = test_df[TARGET]

    X_train = train_df.drop(columns=[TARGET])
    X_val = val_df.drop(columns=[TARGET])
    X_test = test_df.drop(columns=[TARGET])

    # Log transform
    y_train = log_transform(y_train_raw)
    y_val = log_transform(y_val_raw)

    # Categóricas
    cat_features = X_train.select_dtypes(include=["object"]).columns.tolist()

    for col in cat_features:
        X_train[col] = X_train[col].astype(str).fillna("NA")
        X_val[col] = X_val[col].astype(str).fillna("NA")
        X_test[col] = X_test[col].astype(str).fillna("NA")

    X_train = X_train.fillna(-999)
    X_val = X_val.fillna(-999)
    X_test = X_test.fillna(-999)

    model = CatBoostRegressor(
        iterations=2500,
        learning_rate=0.03,
        depth=8,
        random_seed=RANDOM_SEED,
        early_stopping_rounds=150,
        verbose=200,
    )

    model.fit(
        X_train,
        y_train,
        cat_features=cat_features,
        eval_set=(X_val, y_val)
    )

    # Smearing
    smearing_factor = 1.0
    if ENABLE_SMEARING:
        residuals = y_train - model.predict(X_train)
        smearing_factor = np.mean(np.exp(residuals))

    # Avaliação Test
    test_preds = inverse_log(model.predict(X_test)) * smearing_factor

    rmse = mean_squared_error(y_test_raw, test_preds) ** 0.5
    mae = mean_absolute_error(y_test_raw, test_preds)
    r2 = r2_score(y_test_raw, test_preds)

    logger.info(f"[TEST V8] RMSE: {rmse:.2f}")
    logger.info(f"[TEST V8] MAE : {mae:.2f}")
    logger.info(f"[TEST V8] R²  : {r2:.4f}")

    # Salvar
    Path("models").mkdir(exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "cat_features": cat_features,
            "smearing_factor": smearing_factor,
            "metrics": {"rmse": rmse, "mae": mae, "r2": r2},
        },
        "models/catboost_v8_multi_year.joblib"
    )

    logger.info("Modelo V8 salvo com sucesso.")


if __name__ == "__main__":
    train_v8()