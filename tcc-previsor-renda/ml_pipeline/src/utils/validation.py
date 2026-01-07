"""
Validações do dataset de acordo com o contrato de dados
"""

import pandas as pd
from typing import List

from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def validate_columns(df: pd.DataFrame, required_columns: List[str]):
    missing = set(required_columns) - set(df.columns)
    if missing:
        logger.error(f"Colunas ausentes no dataset: {missing}")
        raise ValueError(f"Colunas ausentes: {missing}")
    logger.info("Validação de colunas concluída com sucesso.")


def validate_not_empty(df: pd.DataFrame):
    if df.empty:
        logger.error("Dataset está vazio.")
        raise ValueError("Dataset vazio.")
    logger.info("Dataset não está vazio.")


def validate_no_null_target(df: pd.DataFrame, target_column: str):
    if df[target_column].isnull().any():
        logger.error("Valores nulos encontrados na variável alvo.")
        raise ValueError("Target contém valores nulos.")
    logger.info("Variável alvo sem valores nulos.")
