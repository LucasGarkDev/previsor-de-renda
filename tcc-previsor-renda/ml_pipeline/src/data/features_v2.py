# ml_pipeline/src/data/features_v2.py
"""
Engenharia de atributos — versão v2
(FEATURE ENGINEERING com variáveis domiciliares e contexto socioeconômico)
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

    # ======================================================
    # Features individuais já existentes
    # ======================================================
    df["idade_squared"] = df["idade"] ** 2

    # ======================================================
    # Normalização de variáveis binárias (PNAD)
    # ======================================================
    # PNAD NÃO usa 1/0 universalmente, então padronizamos
    BIN_MAP = {
        1: 1, 2: 0,
        "1": 1, "2": 0,
        "Sim": 1, "Não": 0,
        "sim": 1, "não": 0,
        True: 1, False: 0,
    }

    bin_cols = [
        "possui_agua_rede",
        "possui_iluminacao_eletrica",
        "possui_geladeira",
        "possui_tv",
        "possui_fogao",
        "possui_radio",
        "zona_urbana",
    ]

    for col in bin_cols:
        if col in df.columns:
            df[col] = df[col].map(BIN_MAP).fillna(0).astype(int)

    # ======================================================
    # Features domiciliares (contexto socioeconômico)
    # ======================================================

    # --------------------------
    # Densidade domiciliar
    # (pessoas por dormitório — padrão em estudos sociais)
    # --------------------------
    df["densidade_domiciliar"] = (
        df["total_pessoas"] /
        df["quantidade_dormitorios"].replace(0, np.nan)
    )

    # Limpeza defensiva
    df["densidade_domiciliar"] = (
        df["densidade_domiciliar"]
        .clip(lower=0, upper=10)
        .fillna(df["densidade_domiciliar"].median())
    )

    # --------------------------
    # Score de infraestrutura básica
    # --------------------------
    infra_cols = [
        "possui_agua_rede",
        "possui_iluminacao_eletrica",
    ]

    df["infraestrutura_score"] = df[infra_cols].sum(axis=1)

    # --------------------------
    # Score de bens duráveis
    # --------------------------
    bens_cols = [
        "possui_geladeira",
        "possui_tv",
        "possui_fogao",
        "possui_radio",
    ]

    df["bens_score"] = df[bens_cols].sum(axis=1)

    # --------------------------
    # Interação capital humano × território
    # --------------------------
    df["anos_estudo_urbano"] = df["anos_estudo"] * df["zona_urbana"]

    # ======================================================
    # Transformação da variável alvo
    # ======================================================
    if APPLY_LOG_TARGET:
        df[f"log_{TARGET_COLUMN}"] = np.log(df[TARGET_COLUMN])

    # ======================================================
    # Persistência
    # ======================================================
    output_path = DATA_PROCESSED_DIR / "v2" / "train_ready.parquet"
    write_parquet(df, output_path)

    logger.info("Engenharia de atributos v2 concluída com sucesso")
    return output_path


if __name__ == "__main__":
    build_features_v2()
