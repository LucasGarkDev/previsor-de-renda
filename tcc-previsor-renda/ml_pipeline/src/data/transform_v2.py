# ml_pipeline/src/data/transform_v2.py
"""
Transformações do dataset v2 (Pessoa + Domicílio)
(TRANSFORM – limpeza e preparação conceitual)
"""

from ml_pipeline.src.config.settings import (
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


def transform_dataset_v2():
    logger.info("Iniciando transformação do dataset v2")

    input_path = DATA_PROCESSED_DIR / "v2" / "pnad_merged.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    # =========================
    # Limpeza da variável alvo
    # =========================
    df = df.dropna(subset=[TARGET_COLUMN])
    df = df[df[TARGET_COLUMN] > 0]

    validate_no_null_target(df, TARGET_COLUMN)

    # =========================
    # Tratamento de outliers
    # =========================
    lower = df[TARGET_COLUMN].quantile(LOWER_INCOME_QUANTILE)
    upper = df[TARGET_COLUMN].quantile(UPPER_INCOME_QUANTILE)

    df = df[(df[TARGET_COLUMN] >= lower) & (df[TARGET_COLUMN] <= upper)]

    # =========================
    # Tratamento explícito de missing domiciliar
    # =========================
    categorical_cols = df.select_dtypes(include=["object"]).columns
    numeric_cols = df.select_dtypes(exclude=["object"]).columns

    for col in categorical_cols:
        df[col] = df[col].fillna("NA_DOM")

    for col in numeric_cols:
        df[col] = df[col].fillna(-1)

    output_path = DATA_PROCESSED_DIR / "v2" / "pnad_transformed.parquet"
    write_parquet(df, output_path)

    logger.info(f"Transformação v2 concluída: {len(df)} registros")
    return output_path


if __name__ == "__main__":
    transform_dataset_v2()
