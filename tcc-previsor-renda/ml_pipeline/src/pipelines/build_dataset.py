# ml_pipeline/src/pipelines/build_dataset.py

"""
Orquestrador do pipeline de dados

Executa, em ordem:
1. Extração da PNAD (BigQuery)
2. Transformação e limpeza
3. Engenharia de atributos
4. Split treino / validação / teste
"""

from ml_pipeline.src.data.extract_bigquery_pessoa import extract_pnad
from ml_pipeline.src.data.transform import transform_dataset
from ml_pipeline.src.data.features import build_features
from ml_pipeline.src.data.split import split_dataset
from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.pipeline_version import PIPELINE_VERSION


logger = get_logger(__name__)


def run_pipeline():
    logger.info("========== INÍCIO DO PIPELINE DE DADOS ==========")
    logger.info(f"Pipeline version: {PIPELINE_VERSION}")

    extract_pnad()
    transform_dataset()
    build_features()
    split_dataset()

    logger.info("========== PIPELINE FINALIZADO COM SUCESSO ==========")


if __name__ == "__main__":
    run_pipeline()
