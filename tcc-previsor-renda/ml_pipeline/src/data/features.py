"""
Engenharia de atributos do modelo
(FEATURE ENGINEERING)
"""

import numpy as np

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    APPLY_LOG_TARGET,
)

from ml_pipeline.src.utils.io import read_parquet, write_parquet
from ml_pipeline.src.utils.validation import validate_not_empty
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def build_features():
    logger.info("Iniciando engenharia de atributos")

    input_path = DATA_PROCESSED_DIR / "pnad_transformed.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    # Feature derivada
    df["idade_squared"] = df["idade"] ** 2

    # Transformação da variável alvo
    if APPLY_LOG_TARGET:
        df[f"log_{TARGET_COLUMN}"] = np.log(df[TARGET_COLUMN])

    output_path = DATA_PROCESSED_DIR / "train_ready.parquet"
    write_parquet(df, output_path)

    logger.info("Engenharia de atributos concluída")
    return output_path


if __name__ == "__main__":
    build_features()
