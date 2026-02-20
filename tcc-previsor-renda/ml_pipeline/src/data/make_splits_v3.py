"""
Criação dos conjuntos Train / Validation / Test — v3
(V6 com Feature Engineering + Split Estratificado + Controle de Outliers)
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    TRAIN_SIZE,
    VALIDATION_SIZE,
    TEST_SIZE,
    RANDOM_SEED,
    LOWER_INCOME_QUANTILE,
    UPPER_INCOME_QUANTILE,
)

from ml_pipeline.src.utils.io import read_parquet, write_parquet
from ml_pipeline.src.utils.validation import validate_not_empty
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.features.feature_engineering_v6 import (
    apply_feature_engineering_v6,
)
from ml_pipeline.src.features.feature_engineering_v7 import (
    apply_feature_engineering_v7,
)

logger = get_logger(__name__)


# ======================================================
# Função auxiliar: criar faixa de renda para estratificação
# ======================================================
def create_income_bins(df: pd.DataFrame, n_bins: int = 5) -> pd.Series:
    return pd.qcut(
        df[TARGET_COLUMN],
        q=n_bins,
        labels=False,
        duplicates="drop"
    )


# ======================================================
# Pipeline principal
# ======================================================
def make_splits_v3():

    logger.info("Iniciando criação de splits v3 (com V6)")

    input_path = DATA_PROCESSED_DIR / "v3" / "pnad_merged_v3.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    logger.info(f"Registros originais: {len(df)}")

    # ======================================================
    # FEATURE ENGINEERING V6
    # ======================================================
    df = apply_feature_engineering_v6(df)
    df = apply_feature_engineering_v7(df)

    # ======================================================
    # Remoção de outliers (quantis)
    # ======================================================
    lower_bound = df[TARGET_COLUMN].quantile(LOWER_INCOME_QUANTILE)
    upper_bound = df[TARGET_COLUMN].quantile(UPPER_INCOME_QUANTILE)

    df = df[
        (df[TARGET_COLUMN] >= lower_bound) &
        (df[TARGET_COLUMN] <= upper_bound)
    ]

    logger.info(f"Registros após remoção de outliers: {len(df)}")

    # ======================================================
    # Criar faixa para estratificação
    # ======================================================
    df["faixa_renda"] = create_income_bins(df)

    # ======================================================
    # Split Train + Temp
    # ======================================================
    train_df, temp_df = train_test_split(
        df,
        train_size=TRAIN_SIZE,
        stratify=df["faixa_renda"],
        random_state=RANDOM_SEED,
    )

    # ======================================================
    # Split Validation + Test
    # ======================================================
    relative_test_size = TEST_SIZE / (TEST_SIZE + VALIDATION_SIZE)

    val_df, test_df = train_test_split(
        temp_df,
        test_size=relative_test_size,
        stratify=temp_df["faixa_renda"],
        random_state=RANDOM_SEED,
    )

    logger.info(f"Train size: {len(train_df)}")
    logger.info(f"Validation size: {len(val_df)}")
    logger.info(f"Test size: {len(test_df)}")

    # ======================================================
    # Remover coluna auxiliar
    # ======================================================
    train_df = train_df.drop(columns=["faixa_renda"])
    val_df = val_df.drop(columns=["faixa_renda"])
    test_df = test_df.drop(columns=["faixa_renda"])

    # ======================================================
    # Persistência
    # ======================================================
    output_dir = DATA_PROCESSED_DIR / "v3"
    output_dir.mkdir(parents=True, exist_ok=True)

    write_parquet(train_df, output_dir / "train.parquet")
    write_parquet(val_df, output_dir / "validation.parquet")
    write_parquet(test_df, output_dir / "test.parquet")

    logger.info("Splits v3 (V6) criados com sucesso")

    return (
        output_dir / "train.parquet",
        output_dir / "validation.parquet",
        output_dir / "test.parquet",
    )


if __name__ == "__main__":
    make_splits_v3()