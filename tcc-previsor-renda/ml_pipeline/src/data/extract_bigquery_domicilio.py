"ml_pipeline/src/data/extract_bigquery_domicilio.py"

"""
Extração de dados da PNAD — nível domicílio
(EXTRACT – BigQuery → data/raw/v2)
"""

from google.cloud import bigquery

from ml_pipeline.src.config.settings import (
    BQ_PROJECT_ID,
    BQ_DATA_PROJECT,
    BQ_DATASET_PNAD,
    BQ_LOCATION,
    DATA_RAW_DIR,
)

from ml_pipeline.src.utils.io import write_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)

# ======================================================
# COLUNAS REAIS DA TABELA microdados_compatibilizados_domicilio
# (conforme dicionário oficial da Base dos Dados)
# ======================================================
DOMICILIO_COLUMNS = [
    # Chave de junção
    "id_domicilio",

    # Infraestrutura
    "possui_agua_rede",
    "tipo_esgoto",
    "lixo_coletado",
    "possui_iluminacao_eletrica",

    # Bens duráveis
    "possui_geladeira",
    "possui_tv",
    "possui_fogao",
    "possui_radio",

    # Composição do domicílio
    "total_pessoas",
    "quantidade_comodos",
    "quantidade_dormitorios",

    # Contexto territorial
    "zona_urbana",
    "regiao_metropolitana",
]

def build_query() -> str:
    columns_sql = ",\n        ".join(DOMICILIO_COLUMNS)

    query = f"""
    SELECT
        {columns_sql}
    FROM `{BQ_DATA_PROJECT}.{BQ_DATASET_PNAD}.microdados_compatibilizados_domicilio`
    """

    return query


def extract_pnad_domicilio():
    logger.info("Iniciando extração da PNAD (nível domicílio)")

    client = bigquery.Client(project=BQ_PROJECT_ID)

    query = build_query()
    job = client.query(query, location=BQ_LOCATION)
    df = job.to_dataframe()

    output_path = DATA_RAW_DIR / "v2" / "pnad_domicilio.parquet"
    write_parquet(df, output_path)

    logger.info(f"Extração domicílio concluída: {len(df)} registros")
    logger.info(f"Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    extract_pnad_domicilio()
