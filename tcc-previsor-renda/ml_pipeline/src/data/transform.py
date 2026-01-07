"""
Transformações básicas do dataset
Limpeza, filtros finais e tratamento de outliers
"""

import pandas as pd

from ml_pipeline.src.config.settings import (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    LOWER_INCOME_QUANTILE,
    UPPER_INCOME_QUANTILE
)


def transform_dataset():
    input_path = DATA_RAW_DIR / "pnad_extract.parquet"
    df = pd.read_parquet(input_path)

    # Remove registros sem renda
    df = df.dropna(subset=[TARGET_COLUMN])

    # Remove rendas negativas ou zero
    df = df[df[TARGET_COLUMN] > 0]

    # Tratamento de outliers por quantis
    lower = df[TARGET_COLUMN].quantile(LOWER_INCOME_QUANTILE)
    upper = df[TARGET_COLUMN].quantile(UPPER_INCOME_QUANTILE)

    df = df[(df[TARGET_COLUMN] >= lower) & (df[TARGET_COLUMN] <= upper)]

    output_path = DATA_PROCESSED_DIR / "pnad_transformed.parquet"
    df.to_parquet(output_path, index=False)

    print(f"Transformação concluída: {len(df)} registros")
    print(f"Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    transform_dataset()
