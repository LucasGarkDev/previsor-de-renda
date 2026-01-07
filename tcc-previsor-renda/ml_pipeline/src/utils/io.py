"""
Funções utilitárias de leitura e escrita de dados
"""

import pandas as pd
from pathlib import Path

from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        logger.error(f"Arquivo não encontrado: {path}")
        raise FileNotFoundError(path)

    logger.info(f"Lendo arquivo: {path}")
    return pd.read_parquet(path)


def write_parquet(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    logger.info(f"Arquivo salvo: {path}")
