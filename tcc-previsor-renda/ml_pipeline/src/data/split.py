"""
Divisão do dataset em treino, validação e teste
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
    STRATIFY_COLUMN
)


def split_dataset():
    input_path = DATA_PROCESSED_DIR / "train_ready.parquet"
    df = pd.read_parquet(input_path)

    # Cria faixas de renda para estratificação
    df[STRATIFY_COLUMN] = pd.qcut(
        df[TARGET_COLUMN],
        q=10,
        duplicates="drop"
    )

    train_df, temp_df = train_test_split(
        df,
        test_size=(1 - TRAIN_SIZE),
        stratify=df[STRATIFY_COLUMN],
        random_state=RANDOM_SEED
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=(TEST_SIZE / (TEST_SIZE + VALIDATION_SIZE)),
        stratify=temp_df[STRATIFY_COLUMN],
        random_state=RANDOM_SEED
    )

    train_df.to_parquet(DATA_PROCESSED_DIR / "train.parquet", index=False)
    val_df.to_parquet(DATA_PROCESSED_DIR / "validation.parquet", index=False)
    test_df.to_parquet(DATA_PROCESSED_DIR / "test.parquet", index=False)

    print("Split concluído:")
    print(f"Treino: {len(train_df)}")
    print(f"Validação: {len(val_df)}")
    print(f"Teste: {len(test_df)}")


if __name__ == "__main__":
    split_dataset()
