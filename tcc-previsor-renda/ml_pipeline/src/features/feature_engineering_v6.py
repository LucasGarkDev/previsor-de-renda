"""
Feature Engineering V6
Objetivo: adicionar interações estruturais para maximizar R²

Features adicionadas:
- idade_quadrado
- experiencia_aprox
- idade_x_estudo
"""

import pandas as pd
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def apply_feature_engineering_v6(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica engenharia de features estruturais V6.
    Retorna dataframe modificado.
    """

    logger.info("Aplicando Feature Engineering V6...")

    df = df.copy()

    # ======================================================
    # 1️⃣ Idade ao quadrado
    # ======================================================
    if "idade" in df.columns:
        df["idade_quadrado"] = df["idade"] ** 2
        logger.info("Feature criada: idade_quadrado")

    # ======================================================
    # 2️⃣ Experiência aproximada
    # experiencia ≈ idade - anos_estudo - 6
    # ======================================================
    if "idade" in df.columns and "anos_estudo" in df.columns:
        df["experiencia_aprox"] = df["idade"] - df["anos_estudo"] - 6
        df["experiencia_aprox"] = df["experiencia_aprox"].clip(lower=0)
        logger.info("Feature criada: experiencia_aprox")

    # ======================================================
    # 3️⃣ Interação idade x anos_estudo
    # ======================================================
    if "idade" in df.columns and "anos_estudo" in df.columns:
        df["idade_x_estudo"] = df["idade"] * df["anos_estudo"]
        logger.info("Feature criada: idade_x_estudo")

    logger.info("Feature Engineering V6 aplicada com sucesso.")

    return df