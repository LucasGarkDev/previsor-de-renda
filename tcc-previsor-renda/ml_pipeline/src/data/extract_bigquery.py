"""
Extração de dados da PNAD tradicional via BigQuery
Salva os dados brutos recortados em data/raw
"""

from google.cloud import bigquery
import pandas as pd

from ml_pipeline.src.config.settings import (
    BQ_PROJECT_ID,
    BQ_DATASET_PNAD,
    BQ_TABLE_PESSOA,
    DATA_RAW_DIR,
    SAMPLE_SIZE,
    MIN_AGE,
    FILTER_OCUPADOS,
    FILTER_TRABALHOU_SEMANA,
    RANDOM_SEED,
    FEATURE_COLUMNS,
    TARGET_COLUMN
)


def build_query() -> str:
    """
    Constrói a query SQL de extração baseada nas configurações globais.
    """
    selected_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    columns_sql = ", ".join(selected_columns)

    where_clauses = [f"idade >= {MIN_AGE}"]

    if FILTER_OCUPADOS:
        where_clauses.append("ocupacao_semana = 1")

    if FILTER_TRABALHOU_SEMANA:
        where_clauses.append("trabalhou_semana = 1")

    where_sql = " AND ".join(where_clauses)

    query = f"""
    SELECT
        {columns_sql}
    FROM `{BQ_DATASET_PNAD}.{BQ_TABLE_PESSOA}`
    WHERE {where_sql}
    ORDER BY RAND({RANDOM_SEED})
    LIMIT {SAMPLE_SIZE}
    """

    return query


def extract_pnad():
    """
    Executa a extração da PNAD e salva o resultado em Parquet.
    """
    client = bigquery.Client(project=BQ_PROJECT_ID)

    query = build_query()
    df = client.query(query).to_dataframe()

    output_path = DATA_RAW_DIR / "pnad_extract.parquet"
    df.to_parquet(output_path, index=False)

    print(f"Extração concluída: {len(df)} registros")
    print(f"Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    extract_pnad()
