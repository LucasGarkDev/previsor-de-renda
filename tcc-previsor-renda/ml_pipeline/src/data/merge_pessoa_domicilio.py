"ml_pipeline/src/data/merge_pessoa_domicilio.py"

"""
Merge pessoa + domicílio
(JOIN explícito e documentado)
"""

import pandas as pd

from ml_pipeline.src.config.settings import DATA_RAW_DIR, DATA_PROCESSED_DIR
from ml_pipeline.src.utils.io import read_parquet, write_parquet
from ml_pipeline.src.utils.validation import validate_not_empty
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def merge_pessoa_domicilio():
    logger.info("Iniciando merge pessoa + domicílio")

    pessoa_path = DATA_RAW_DIR / "v2" / "pnad_pessoa.parquet"
    domicilio_path = DATA_RAW_DIR / "v2" / "pnad_domicilio.parquet"

    df_pessoa = read_parquet(pessoa_path)
    df_domicilio = read_parquet(domicilio_path)

    validate_not_empty(df_pessoa)
    validate_not_empty(df_domicilio)

    logger.info("Executando LEFT JOIN por id_domicilio")

    df_merged = df_pessoa.merge(
        df_domicilio,
        on="id_domicilio",
        how="left",
        validate="many_to_one"
    )

    logger.info(f"Dataset após merge: {len(df_merged)} registros")

    output_path = DATA_PROCESSED_DIR / "v2" / "pnad_merged.parquet"
    write_parquet(df_merged, output_path)

    logger.info(f"Merge concluído. Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    merge_pessoa_domicilio()
