"""
Diagnóstico completo do universo da PNAD no BigQuery
Investiga volume total, por ano e impacto dos filtros
"""

from google.cloud import bigquery

from ml_pipeline.src.config.settings import (
    BQ_PROJECT_ID,
    BQ_DATA_PROJECT,
    BQ_DATASET_PNAD,
    BQ_LOCATION,
    MIN_AGE,
)

from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


TABLE = f"{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.microdados_compatibilizados_pessoa"


def run_query(client, query: str, description: str):
    logger.info(f"\n--- {description} ---")
    job = client.query(query, location=BQ_LOCATION)
    result = job.result()
    for row in result:
        logger.info(row)


def diagnose_universe():
    logger.info("Iniciando diagnóstico do universo PNAD")

    client = bigquery.Client(project=BQ_PROJECT_ID)

    # ======================================================
    # 1. Total geral
    # ======================================================
    query_total = f"""
    SELECT COUNT(*) AS total_registros
    FROM `{TABLE}`
    """
    run_query(client, query_total, "Total geral da tabela pessoa")

    # ======================================================
    # 2. Total por ano
    # ======================================================
    query_por_ano = f"""
    SELECT ano, COUNT(*) AS total
    FROM `{TABLE}`
    GROUP BY ano
    ORDER BY ano
    """
    run_query(client, query_por_ano, "Total por ano")

    # ======================================================
    # 3. Total idade >= MIN_AGE
    # ======================================================
    query_idade = f"""
    SELECT COUNT(*) AS total_maiores_18
    FROM `{TABLE}`
    WHERE idade >= {MIN_AGE}
    """
    run_query(client, query_idade, "Total com idade >= 18")

    # ======================================================
    # 4. Impacto ocupacao_semana
    # ======================================================
    query_ocupacao = f"""
    SELECT ocupacao_semana, COUNT(*) AS total
    FROM `{TABLE}`
    GROUP BY ocupacao_semana
    ORDER BY total DESC
    """
    run_query(client, query_ocupacao, "Distribuição ocupacao_semana")

    # ======================================================
    # 5. Impacto trabalhou_semana (ver tipo real)
    # ======================================================
    query_trabalhou = f"""
    SELECT trabalhou_semana, COUNT(*) AS total
    FROM `{TABLE}`
    GROUP BY trabalhou_semana
    ORDER BY total DESC
    """
    run_query(client, query_trabalhou, "Distribuição trabalhou_semana")

    # ======================================================
    # 6. Filtros combinados
    # ======================================================
    query_filtros = f"""
    SELECT COUNT(*) AS total_filtrado
    FROM `{TABLE}`
    WHERE idade >= {MIN_AGE}
      AND ocupacao_semana = 1
      AND trabalhou_semana = 1
    """
    run_query(client, query_filtros, "Total após TODOS filtros (numeric 1)")

    query_filtros_string = f"""
    SELECT COUNT(*) AS total_filtrado_string
    FROM `{TABLE}`
    WHERE idade >= {MIN_AGE}
      AND ocupacao_semana = 1
      AND trabalhou_semana = '1'
    """
    run_query(client, query_filtros_string, "Total após TODOS filtros (string '1')")

    logger.info("\nDiagnóstico concluído.")


if __name__ == "__main__":
    diagnose_universe()