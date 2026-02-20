"""
Estimador de capacidade do BigQuery
Avalia diferentes LIMITs usando dry-run
(Não executa query real)
"""

from google.cloud import bigquery

from ml_pipeline.src.config.settings import (
    BQ_PROJECT_ID,
    BQ_DATA_PROJECT,
    BQ_DATASET_PNAD,
    BQ_LOCATION,
    MIN_AGE,
    FILTER_OCUPADOS,
    FILTER_TRABALHOU_SEMANA,
)

from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


# ======================================================
# LIMITS QUE QUEREMOS TESTAR
# ======================================================
TEST_LIMITS = [5_000, 10_000, 25_000, 50_000, 100_000, 200_000]


def build_query(limit: int) -> str:
    where_clauses = [f"p.idade >= {MIN_AGE}"]

    if FILTER_OCUPADOS:
        where_clauses.append("p.ocupacao_semana = 1")

    if FILTER_TRABALHOU_SEMANA:
        where_clauses.append("p.trabalhou_semana = '1'")

    where_sql = " AND ".join(where_clauses)

    query = f"""
    SELECT
        p.id_domicilio,
        p.anos_estudo,
        p.idade,
        p.sexo,
        p.raca_cor,
        p.horas_trabalhadas_semana,
        p.renda_mensal_ocupacao_principal_deflacionado
    FROM `{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.microdados_compatibilizados_pessoa` p
    WHERE {where_sql}
    ORDER BY RAND()
    LIMIT {limit}
    """

    return query


def estimate_limits():
    logger.info("Estimando capacidade segura do BigQuery (dry-run)")

    client = bigquery.Client(project=BQ_PROJECT_ID)

    for limit in TEST_LIMITS:
        query = build_query(limit)

        job_config = bigquery.QueryJobConfig(
            dry_run=True,
            use_query_cache=False,
        )

        job = client.query(query, job_config=job_config)

        gb_processed = job.total_bytes_processed / (1024 ** 3)

        status = "🟢 Seguro"
        if gb_processed > 5:
            status = "🟡 Moderado"
        if gb_processed > 10:
            status = "🔴 Alto"

        logger.info(
            f"LIMIT {limit:>7} → "
            f"{gb_processed:6.3f} GB processados → {status}"
        )

    logger.info("Estimativa concluída.")


if __name__ == "__main__":
    estimate_limits()