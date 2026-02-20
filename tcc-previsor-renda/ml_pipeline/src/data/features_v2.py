# ml_pipeline/src/data/features_v2.py
"""
Engenharia de atributos — versão v2 (ATUALIZADO)
(FEATURE ENGINEERING com variáveis domiciliares e contexto socioeconômico)

Novidades:
- Interações estruturais para capturar heterogeneidade (sexo, urbano, região metropolitana, carteira)
- Proteções contra NaN/inf em divisões e logs
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


def _safe_col(df, col: str, default=0):
    """Garante existência de coluna no df (evita quebrar pipeline)."""
    if col not in df.columns:
        df[col] = default
    return df[col]


def build_features_v2():
    logger.info("Iniciando engenharia de atributos v2 (ATUALIZADO)")

    input_path = DATA_PROCESSED_DIR / "v2" / "pnad_transformed.parquet"
    df = read_parquet(input_path)

    validate_not_empty(df)

    # ======================================================
    # Features individuais já existentes
    # ======================================================
    if "idade" in df.columns:
        df["idade_squared"] = df["idade"] ** 2
    else:
        df["idade_squared"] = 0

    # ======================================================
    # Normalização de variáveis binárias (PNAD)
    # ======================================================
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
        "possui_carteira_assinada",
        "trabalhou_semana",
        "sabe_ler_escrever",
    ]

    for col in bin_cols:
        if col in df.columns:
            df[col] = df[col].map(BIN_MAP).fillna(0).astype(int)

    # ======================================================
    # Features domiciliares (contexto socioeconômico)
    # ======================================================
    # Garantir colunas de domicílio (caso venham faltando por mudanças no extract)
    _safe_col(df, "total_pessoas", default=np.nan)
    _safe_col(df, "quantidade_dormitorios", default=np.nan)

    # --------------------------
    # Densidade domiciliar (pessoas por dormitório)
    # --------------------------
    denom = df["quantidade_dormitorios"].replace(0, np.nan)
    df["densidade_domiciliar"] = df["total_pessoas"] / denom

    df["densidade_domiciliar"] = (
        df["densidade_domiciliar"]
        .replace([np.inf, -np.inf], np.nan)
        .clip(lower=0, upper=10)
    )

    # fallback robusto
    if df["densidade_domiciliar"].isna().all():
        df["densidade_domiciliar"] = 0
    else:
        df["densidade_domiciliar"] = df["densidade_domiciliar"].fillna(
            df["densidade_domiciliar"].median()
        )

    # --------------------------
    # Score de infraestrutura básica
    # --------------------------
    infra_cols = [c for c in ["possui_agua_rede", "possui_iluminacao_eletrica"] if c in df.columns]
    df["infraestrutura_score"] = df[infra_cols].sum(axis=1) if infra_cols else 0

    # --------------------------
    # Score de bens duráveis
    # --------------------------
    bens_cols = [c for c in ["possui_geladeira", "possui_tv", "possui_fogao", "possui_radio"] if c in df.columns]
    df["bens_score"] = df[bens_cols].sum(axis=1) if bens_cols else 0

    # ======================================================
    # Interações estruturais (NOVAS)
    # ======================================================
    # Base: garantir colunas
    _safe_col(df, "anos_estudo", default=0)
    _safe_col(df, "zona_urbana", default=0)
    _safe_col(df, "sexo", default=0)  # pode ser categórica; aqui só tratamos o caso numérico
    _safe_col(df, "regiao_metropolitana", default=0)
    _safe_col(df, "horas_trabalhadas_semana", default=0)
    _safe_col(df, "possui_carteira_assinada", default=0)

    # 1) Capital humano × urbano
    df["anos_estudo_urbano"] = df["anos_estudo"] * df["zona_urbana"]

    # 2) Capital humano × metrópole
    df["anos_estudo_metro"] = df["anos_estudo"] * df["regiao_metropolitana"]

    # 3) Horas × carteira (formalidade)
    df["horas_carteira"] = df["horas_trabalhadas_semana"] * df["possui_carteira_assinada"]

    # 4) Idade × horas (ciclo de vida / esforço)
    if "idade" in df.columns:
        df["idade_horas"] = df["idade"] * df["horas_trabalhadas_semana"]
    else:
        df["idade_horas"] = 0

    # 5) Bens × urbano (proxy de capital material em contexto urbano)
    df["bens_urbano"] = df["bens_score"] * df["zona_urbana"]

    # 6) Infra × urbano (infraestrutura com efeito diferente em urbano)
    df["infra_urbano"] = df["infraestrutura_score"] * df["zona_urbana"]

    # ======================================================
    # Transformação da variável alvo (opcional)
    # ======================================================
    if APPLY_LOG_TARGET:
        # log seguro: renda > 0 já foi garantida no transform_v2
        df[f"log_{TARGET_COLUMN}"] = np.log(df[TARGET_COLUMN])

    # ======================================================
    # Persistência
    # ======================================================
    output_path = DATA_PROCESSED_DIR / "v2" / "train_ready.parquet"
    write_parquet(df, output_path)

    logger.info("Engenharia de atributos v2 concluída com sucesso (ATUALIZADO)")
    logger.info(f"Shape final: {df.shape[0]} linhas, {df.shape[1]} colunas")

    return output_path


if __name__ == "__main__":
    build_features_v2()