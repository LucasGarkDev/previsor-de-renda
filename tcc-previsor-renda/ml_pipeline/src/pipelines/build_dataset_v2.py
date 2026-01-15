# ml_pipeline/src/pipelines/build_dataset_v2.py

"""
Orquestrador do pipeline de dados — versão v2

Pipeline v2:
1. Extração PNAD (Pessoa)
2. Extração PNAD (Domicílio)
3. Merge Pessoa + Domicílio
4. Transformação e limpeza (v2)
5. Engenharia de atributos (v2)
6. Split treino / validação / teste (v2)
"""

from ml_pipeline.src.data.extract_bigquery_pessoa import extract_pnad_pessoa
from ml_pipeline.src.data.extract_bigquery_domicilio import extract_pnad_domicilio
from ml_pipeline.src.data.merge_pessoa_domicilio import merge_pessoa_domicilio

from ml_pipeline.src.data.transform_v2 import transform_dataset_v2
from ml_pipeline.src.data.features_v2 import build_features_v2
from ml_pipeline.src.data.split_v2 import split_dataset_v2

from ml_pipeline.src.utils.logging import get_logger
from ml_pipeline.src.config.pipeline_version import PIPELINE_VERSION

logger = get_logger(__name__)


def run_pipeline_v2():
    logger.info("========== INÍCIO DO PIPELINE DE DADOS (V2) ==========")
    logger.info(f"Pipeline version: {PIPELINE_VERSION}")

    # =========================
    # Extração
    # =========================
    extract_pnad_pessoa()
    extract_pnad_domicilio()

    # =========================
    # Merge
    # =========================
    merge_pessoa_domicilio()

    # =========================
    # Transformação e features
    # =========================
    transform_dataset_v2()
    build_features_v2()

    # =========================
    # Split
    # =========================
    split_dataset_v2()

    logger.info("========== PIPELINE V2 FINALIZADO COM SUCESSO ==========")


if __name__ == "__main__":
    run_pipeline_v2()
