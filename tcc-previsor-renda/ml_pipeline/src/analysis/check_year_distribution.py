"""
Análise de distribuição temporal da base PNAD
Verifica se estamos usando 1 ou múltiplos anos
"""

import pandas as pd
from collections import Counter

from ml_pipeline.src.config.settings import DATA_PROCESSED_DIR
from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def check_year_distribution():

    logger.info("Iniciando análise de distribuição por ano")

    base_path = DATA_PROCESSED_DIR / "v3" / "pnad_merged_v3.parquet"
    df = read_parquet(base_path)

    logger.info(f"Total de registros: {len(df)}")

    # ======================================================
    # 1️⃣ Detectar coluna de ano automaticamente
    # ======================================================

    possible_year_cols = [
        col for col in df.columns
        if "ano" in col.lower()
        or "year" in col.lower()
        or col.lower() in ["ano", "year"]
    ]

    if not possible_year_cols:
        logger.warning("Nenhuma coluna de ano encontrada automaticamente.")
        print("\n⚠️ Nenhuma coluna identificada como ano.")
        print("Colunas disponíveis:")
        print(df.columns.tolist())
        return

    print("\nColunas candidatas a 'ano':")
    for col in possible_year_cols:
        print(f"- {col}")

    # ======================================================
    # 2️⃣ Para cada possível coluna de ano
    # ======================================================

    for year_col in possible_year_cols:

        print("\n" + "="*50)
        print(f"ANÁLISE PARA COLUNA: {year_col}")
        print("="*50)

        unique_years = sorted(df[year_col].dropna().unique())

        print(f"\nAnos únicos encontrados ({len(unique_years)}):")
        print(unique_years)

        year_counts = (
            df[year_col]
            .value_counts()
            .sort_index()
        )

        print("\nDistribuição por ano:")
        print(year_counts)

        print("\nPercentual por ano:")
        percent = (year_counts / len(df) * 100).round(2)
        print(percent)

    logger.info("Análise concluída.")


if __name__ == "__main__":
    check_year_distribution()