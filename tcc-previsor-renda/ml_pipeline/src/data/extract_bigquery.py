"ml_pipeline/src/data/extract_bigquery.py"
"""
Extração de dados da PNAD tradicional via BigQuery
(EXTRACT – BigQuery → data/raw)
"""

from google.cloud import bigquery

from ml_pipeline.src.config.settings import (
    BQ_PROJECT_ID,
    BQ_DATA_PROJECT,
    BQ_DATASET_PNAD,
    BQ_TABLE_PESSOA,
    BQ_LOCATION,
    DATA_RAW_DIR,
    SAMPLE_SIZE,
    MIN_AGE,
    FILTER_OCUPADOS,
    FILTER_TRABALHOU_SEMANA,
    RANDOM_SEED,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    PNAD_COLUMN_MAP,
)

from ml_pipeline.src.utils.io import write_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def build_query() -> str:
    """
    Constrói a query SQL usando o mapa conceitual → técnico da PNAD.
    """

    # SELECT com alias conceitual
    select_expressions = [
        f"{PNAD_COLUMN_MAP[col]} AS {col}"
        for col in FEATURE_COLUMNS
    ]

    # Variável alvo (nome técnico correto)
    select_expressions.append(
        f"{TARGET_COLUMN} AS {TARGET_COLUMN}"
    )

    columns_sql = ",\n        ".join(select_expressions)

    # WHERE – SEMPRE com nomes técnicos
    where_clauses = [f"idade >= {MIN_AGE}"]

    if FILTER_OCUPADOS:
        # ocupacao_semana é INTEGER
        where_clauses.append("ocupacao_semana = 1")

    if FILTER_TRABALHOU_SEMANA:
        # trabalhou_semana é STRING
        where_clauses.append("trabalhou_semana = '1'")

    where_sql = " AND ".join(where_clauses)

    query = f"""
    SELECT
        {columns_sql}
    FROM `{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.{BQ_TABLE_PESSOA}`
    WHERE {where_sql}
    ORDER BY RAND()
    LIMIT {SAMPLE_SIZE}
    """
    return query


def extract_pnad():
    logger.info("Iniciando extração da PNAD via BigQuery")

    client = bigquery.Client(project=BQ_PROJECT_ID)

    query = build_query()

    job = client.query(
        query,
        location=BQ_LOCATION
    )

    df = job.to_dataframe()

    output_path = DATA_RAW_DIR / "pnad_extract.parquet"
    write_parquet(df, output_path)

    logger.info(f"Extração concluída com {len(df)} registros")
    logger.info(f"Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    extract_pnad()
