"""
Feature Engineering V7
Interações estruturais guiadas por feature importance
"""

import pandas as pd
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def apply_feature_engineering_v7(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica interações estruturais V7.
    """

    logger.info("Aplicando Feature Engineering V7...")

    df = df.copy()

    # =========================
    # Escolaridade x Horas trabalhadas
    # =========================
    if "anos_estudo" in df.columns and "horas_trabalhadas_semana" in df.columns:
        df["estudo_x_horas"] = (
            df["anos_estudo"] * df["horas_trabalhadas_semana"]
        )
        logger.info("Feature criada: estudo_x_horas")

    # =========================
    # Escolaridade x Carteira assinada
    # =========================
    if "anos_estudo" in df.columns and "possui_carteira_assinada" in df.columns:
        # Converter para numérico se necessário
        carteira = df["possui_carteira_assinada"]
        if carteira.dtype == "object":
            carteira = carteira.astype(str).map({"1": 1, "0": 0, "Sim": 1, "Não": 0})
        df["estudo_x_carteira"] = df["anos_estudo"] * carteira.fillna(0)
        logger.info("Feature criada: estudo_x_carteira")

    # =========================
    # Idade x Horas trabalhadas
    # =========================
    if "idade" in df.columns and "horas_trabalhadas_semana" in df.columns:
        df["idade_x_horas"] = (
            df["idade"] * df["horas_trabalhadas_semana"]
        )
        logger.info("Feature criada: idade_x_horas")

    logger.info("Feature Engineering V7 aplicada com sucesso.")

    return df