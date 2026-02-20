"""
Extração PNAD v8 — Multi-Ano (2015–2024)
Processamento 100% no BigQuery
Amostragem balanceada por ano
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


YEARS_START = 2015
YEARS_END = 2024


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
        [
            "p.id_domicilio",
            "p.ano",
            "p.trimestre",
        ]
        + pessoa_features_sql
        + domicilio_features_sql
        + [
            f"p.{TARGET_COLUMN} AS {TARGET_COLUMN}",
            # ==========================
            # Features temporais V8
            # ==========================
            "p.ano - 2015 AS ano_normalizado",
            "IF(p.ano IN (2020, 2021), 1, 0) AS dummy_pandemia",
            "p.ano + (p.trimestre - 1) / 4.0 AS tempo_continuo",
        ]
    )

    select_sql = ",\n        ".join(select_parts)

    where_clauses = [
        f"p.idade >= {MIN_AGE}",
        f"p.ano BETWEEN {YEARS_START} AND {YEARS_END}"
    ]

    if FILTER_TRABALHOU_SEMANA:
        where_clauses.append("p.trabalhou_semana = '1'")

    where_sql = " AND ".join(where_clauses)

    # ==========================
    # Amostragem balanceada por ano
    # ==========================
    query = f"""
    SELECT *
    FROM (
        SELECT
            {select_sql},
            ROW_NUMBER() OVER (
                PARTITION BY p.ano
                ORDER BY RAND()
            ) AS rn
        FROM `{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.microdados_compatibilizados_pessoa` p
        LEFT JOIN `{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.microdados_compatibilizados_domicilio` d
            ON p.id_domicilio = d.id_domicilio
        WHERE {where_sql}
    )
    WHERE rn <= {SAMPLE_SIZE}
    """

    return query


def extract_pnad_merged_v8():

    logger.info("Iniciando extração PNAD v8 (Multi-Ano)")

    client = bigquery.Client(project=BQ_PROJECT_ID)

    query = build_query()

    # ==========================
    # Dry-run
    # ==========================
    job_config = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False
    )

    dry_run_job = client.query(query, job_config=job_config)
    processed_gb = dry_run_job.total_bytes_processed / (1024**3)

    logger.info(
        f"Query irá processar aproximadamente {processed_gb:.4f} GB"
    )

    if processed_gb > 8:
        raise RuntimeError(
            f"Query muito pesada ({processed_gb:.2f} GB). "
            "Revise filtros ou SAMPLE_SIZE."
        )

    # ==========================
    # Execução real
    # ==========================
    job = client.query(query, location=BQ_LOCATION)
    df = job.to_dataframe()

    output_path = DATA_PROCESSED_DIR / "v8" / "pnad_merged_v8.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    write_parquet(df, output_path)

    logger.info(f"Extração v8 concluída: {len(df)} registros")
    logger.info(f"Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    extract_pnad_merged_v8()