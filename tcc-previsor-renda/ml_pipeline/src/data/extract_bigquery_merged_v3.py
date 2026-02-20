"""
Extração PNAD com JOIN no BigQuery
(EXTRACT v3 – processamento 100% no servidor)

Versão metodologicamente corrigida:
- Remove filtro incorreto ocupacao_semana = 1
- Usa apenas trabalhou_semana = '1'
"""

from google.cloud import bigquery

from ml_pipeline.src.config.settings import (
    BQ_PROJECT_ID,
    BQ_DATA_PROJECT,
    BQ_DATASET_PNAD,
    BQ_LOCATION,
    DATA_PROCESSED_DIR,
    SAMPLE_SIZE,
    MIN_AGE,
    FILTER_TRABALHOU_SEMANA,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    PNAD_COLUMN_MAP,
)

from ml_pipeline.src.utils.io import write_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


# ======================================================
# COLUNAS DOMICILIARES DISPONÍVEIS
# ======================================================
DOMICILIO_COLUMNS = [
    "possui_agua_rede",
    "tipo_esgoto",
    "lixo_coletado",
    "possui_iluminacao_eletrica",
    "possui_geladeira",
    "possui_tv",
    "possui_fogao",
    "possui_radio",
    "total_pessoas",
    "quantidade_comodos",
    "quantidade_dormitorios",
    "zona_urbana",
    "regiao_metropolitana",
]


def build_query() -> str:
    """
    Query com JOIN direto no BigQuery
    Separando explicitamente variáveis de pessoa e domicílio
    """

    pessoa_features_sql = []
    domicilio_features_sql = []

    for col in FEATURE_COLUMNS:
        if col in PNAD_COLUMN_MAP:
            pessoa_features_sql.append(
                f"p.{PNAD_COLUMN_MAP[col]} AS {col}"
            )
        elif col in DOMICILIO_COLUMNS:
            domicilio_features_sql.append(
                f"d.{col} AS {col}"
            )

    select_parts = (
        ["p.id_domicilio"]
        + pessoa_features_sql
        + domicilio_features_sql
        + [f"p.{TARGET_COLUMN} AS {TARGET_COLUMN}"]
    )

    select_sql = ",\n        ".join(select_parts)

    # ======================================================
    # Filtros metodológicos CORRETOS
    # ======================================================
    where_clauses = [f"p.idade >= {MIN_AGE}"]

    # Trabalhou na semana (é STRING!)
    if FILTER_TRABALHOU_SEMANA:
        where_clauses.append("p.trabalhou_semana = '1'")

    where_sql = " AND ".join(where_clauses)

    # ======================================================
    # Query final
    # ======================================================
    query = f"""
    SELECT
        {select_sql}
    FROM `{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.microdados_compatibilizados_pessoa` p
    LEFT JOIN `{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.microdados_compatibilizados_domicilio` d
        ON p.id_domicilio = d.id_domicilio
    WHERE {where_sql}
    ORDER BY RAND()
    LIMIT {SAMPLE_SIZE}
    """

    return query


def extract_pnad_merged_v3():
    logger.info("Iniciando extração PNAD v3 (JOIN no BigQuery)")
    logger.info(f"SAMPLE_SIZE solicitado: {SAMPLE_SIZE}")

    client = bigquery.Client(project=BQ_PROJECT_ID)

    query = build_query()

    # ======================================================
    # Dry-run para estimar custo
    # ======================================================
    job_config = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False
    )

    dry_run_job = client.query(query, job_config=job_config)
    processed_gb = dry_run_job.total_bytes_processed / (1024**3)

    logger.info(
        f"Query irá processar aproximadamente {processed_gb:.4f} GB"
    )

    # Segurança: aborta se passar de 5GB
    if processed_gb > 5:
        raise RuntimeError(
            f"Query muito pesada ({processed_gb:.2f} GB). "
            "Revise colunas ou filtros antes de executar."
        )

    # ======================================================
    # Execução real
    # ======================================================
    job = client.query(query, location=BQ_LOCATION)
    df = job.to_dataframe()

    if len(df) < SAMPLE_SIZE:
        logger.warning(
            f"Foram retornados apenas {len(df)} registros "
            f"(menor que SAMPLE_SIZE={SAMPLE_SIZE})."
        )

    output_path = DATA_PROCESSED_DIR / "v3" / "pnad_merged_v3.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    write_parquet(df, output_path)

    logger.info(f"Extração v3 concluída: {len(df)} registros")
    logger.info(f"Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    extract_pnad_merged_v3()