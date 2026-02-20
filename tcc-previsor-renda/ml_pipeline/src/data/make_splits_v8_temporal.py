"""
Criação dos conjuntos Train / Validation / Test — V8
Split temporal (realista)
"""

from ml_pipeline.src.config.settings import DATA_PROCESSED_DIR
from ml_pipeline.src.utils.io import read_parquet, write_parquet
from ml_pipeline.src.utils.validation import validate_not_empty
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def make_splits_v8_temporal():

    logger.info("Iniciando criação de splits V8 (temporal)")

    input_path = DATA_PROCESSED_DIR / "v8" / "pnad_merged_v8.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    logger.info(f"Total registros carregados: {len(df)}")

    # ==========================
    # Split temporal
    # ==========================
    train_df = df[df["ano"] <= 2022]
    val_df = df[df["ano"] == 2023]
    test_df = df[df["ano"] == 2024]

    logger.info(f"Train size: {len(train_df)}")
    logger.info(f"Validation size: {len(val_df)}")
    logger.info(f"Test size: {len(test_df)}")

    # ==========================
    # Persistência
    # ==========================
    output_dir = DATA_PROCESSED_DIR / "v8"
    output_dir.mkdir(parents=True, exist_ok=True)

    write_parquet(train_df, output_dir / "train.parquet")
    write_parquet(val_df, output_dir / "validation.parquet")
    write_parquet(test_df, output_dir / "test.parquet")

    logger.info("Splits V8 criados com sucesso.")

    return (
        output_dir / "train.parquet",
        output_dir / "validation.parquet",
        output_dir / "test.parquet",
    )


if __name__ == "__main__":
    make_splits_v8_temporal()