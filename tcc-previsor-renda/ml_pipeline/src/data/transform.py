"""
Transformações básicas do dataset
(TRANSFORM – limpeza e preparação conceitual)
"""

from ml_pipeline.src.config.settings import (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    LOWER_INCOME_QUANTILE,
    UPPER_INCOME_QUANTILE,
)

from ml_pipeline.src.utils.io import read_parquet, write_parquet
from ml_pipeline.src.utils.validation import (
    validate_not_empty,
    validate_no_null_target,
)
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def transform_dataset():
    logger.info("Iniciando transformação do dataset")

    input_path = DATA_RAW_DIR / "pnad_extract.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    # Remove registros sem renda
    df = df.dropna(subset=[TARGET_COLUMN])

    # Remove rendas inválidas
    df = df[df[TARGET_COLUMN] > 0]

    validate_no_null_target(df, TARGET_COLUMN)

    # Tratamento de outliers
    lower = df[TARGET_COLUMN].quantile(LOWER_INCOME_QUANTILE)
    upper = df[TARGET_COLUMN].quantile(UPPER_INCOME_QUANTILE)

    df = df[(df[TARGET_COLUMN] >= lower) & (df[TARGET_COLUMN] <= upper)]

    output_path = DATA_PROCESSED_DIR / "pnad_transformed.parquet"
    write_parquet(df, output_path)

    logger.info(f"Transformação concluída: {len(df)} registros")
    return output_path


if __name__ == "__main__":
    transform_dataset()
