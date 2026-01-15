# ml_pipeline/src/data/features_v2.py

"""
Engenharia de atributos — versão v2
(FEATURE ENGINEERING com variáveis domiciliares)
"""

import numpy as np

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    APPLY_LOG_TARGET,
)

from ml_pipeline.src.utils.io import read_parquet, write_parquet
from ml_pipeline.src.utils.validation import validate_not_empty
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def build_features_v2():
    logger.info("Iniciando engenharia de atributos v2")

    input_path = DATA_PROCESSED_DIR / "v2" / "pnad_transformed.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    # =========================
    # Features já existentes
    # =========================
    df["idade_squared"] = df["idade"] ** 2

    # =========================
    # Features domiciliares
    # =========================

    # Densidade domiciliar
    df["densidade_domiciliar"] = df["total_pessoas"] / df["quantidade_comodos"].replace(0, np.nan)
    df["densidade_domiciliar"] = df["densidade_domiciliar"].fillna(0)

    # Score de infraestrutura básica
    infra_cols = [
        "possui_agua_rede",
        "possui_iluminacao_eletrica",
        "lixo_coletado",
    ]
    df["infraestrutura_score"] = df[infra_cols].apply(
        lambda row: sum(row == 1), axis=1
    )

    # Score de bens duráveis
    bens_cols = [
        "possui_geladeira",
        "possui_tv",
        "possui_fogao",
        "possui_radio",
    ]
    df["bens_score"] = df[bens_cols].apply(
        lambda row: sum(row == 1), axis=1
    )

    # Interação capital humano × território
    df["anos_estudo_urbano"] = df["anos_estudo"] * (df["zona_urbana"] == 1)

    # =========================
    # Transformação do target
    # =========================
    if APPLY_LOG_TARGET:
        df[f"log_{TARGET_COLUMN}"] = np.log(df[TARGET_COLUMN])

    output_path = DATA_PROCESSED_DIR / "v2" / "train_ready.parquet"
    write_parquet(df, output_path)

    logger.info("Engenharia de atributos v2 concluída")
    return output_path


if __name__ == "__main__":
    build_features_v2()
