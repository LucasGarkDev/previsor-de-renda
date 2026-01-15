# ml_pipeline/src/data/split_v2.py

"""
Divisão treino / validação / teste — versão v2
"""

import pandas as pd
from sklearn.model_selection import train_test_split

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    TRAIN_SIZE,
    VALIDATION_SIZE,
    TEST_SIZE,
    RANDOM_SEED,
    STRATIFY_COLUMN,
)

from ml_pipeline.src.utils.io import read_parquet, write_parquet
from ml_pipeline.src.utils.validation import validate_not_empty
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def split_dataset_v2():
    logger.info("Iniciando split treino/validação/teste v2")

    input_path = DATA_PROCESSED_DIR / "v2" / "train_ready.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    # Faixas de renda para estratificação
    df[STRATIFY_COLUMN] = pd.qcut(
        df[TARGET_COLUMN],
        q=10,
        duplicates="drop",
    )

    train_df, temp_df = train_test_split(
        df,
        test_size=(1 - TRAIN_SIZE),
        stratify=df[STRATIFY_COLUMN],
        random_state=RANDOM_SEED,
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=(TEST_SIZE / (TEST_SIZE + VALIDATION_SIZE)),
        stratify=temp_df[STRATIFY_COLUMN],
        random_state=RANDOM_SEED,
    )

    train_df = train_df.drop(columns=[STRATIFY_COLUMN])
    val_df = val_df.drop(columns=[STRATIFY_COLUMN])
    test_df = test_df.drop(columns=[STRATIFY_COLUMN])

    write_parquet(train_df, DATA_PROCESSED_DIR / "v2" / "train.parquet")
    write_parquet(val_df, DATA_PROCESSED_DIR / "v2" / "validation.parquet")
    write_parquet(test_df, DATA_PROCESSED_DIR / "v2" / "test.parquet")

    logger.info(
        f"Split v2 concluído — Treino: {len(train_df)}, "
        f"Validação: {len(val_df)}, Teste: {len(test_df)}"
    )


if __name__ == "__main__":
    split_dataset_v2()
