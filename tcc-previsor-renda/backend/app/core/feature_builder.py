from __future__ import annotations

import pandas as pd

from backend.app.schemas.predict import PredictInput

RACA_COR_MAP = {
    "branca": "2",
    "preta": "4",
    "parda": "6",
    "amarela": "8",
    "indigena": "8",
}

GRAU_FREQUENTADO_MAP = {
    "fundamental_incompleto": "1",
    "fundamental_completo": "2",
    "medio_incompleto": "3",
    "medio_completo": "4",
    "superior_incompleto": "5",
    "superior_completo": "6",
}

POSICAO_OCUPACAO_MAP = {
    "empregado": "3",
    "empregador": "1",
    "conta_propria": "2",
    "outro": "4",
}


def build_model_features(data: PredictInput) -> pd.DataFrame:
    idade = data.idade
    anos_estudo = data.anos_estudo
    experiencia_aprox = max(0, idade - anos_estudo - 6)
    idade_quadrado = idade ** 2
    horas_trabalhadas = data.horas_trabalhadas_semana
    carteira_flag = 1 if data.possui_carteira_assinada else 0

    features = {
        "anos_estudo": anos_estudo,
        "ultimo_grau_frequentado": GRAU_FREQUENTADO_MAP[data.ultimo_grau_frequentado],
        "sabe_ler_escrever": "1" if data.sabe_ler_escrever else "0",
        "idade": idade,
        "sexo": "1" if data.sexo == "masculino" else "0",
        "raca_cor": RACA_COR_MAP[data.raca_cor],
        "trabalhou_semana": "1" if data.trabalhou_semana else "0",
        "ocupacao_semana": 1 if data.ocupacao_semana else 0,
        "atividade_ramo_negocio_semana": data.atividade_ramo_negocio_semana,
        "posicao_ocupacao": POSICAO_OCUPACAO_MAP[data.posicao_ocupacao],
        "possui_carteira_assinada": "1" if data.possui_carteira_assinada else "0",
        "horas_trabalhadas_semana": horas_trabalhadas,
        "sigla_uf": data.sigla_uf.upper(),
        "regiao": _map_regiao(data.sigla_uf.upper()),
        "zona_urbana": 1 if data.zona_urbana else 0,
        "regiao_metropolitana": 1 if data.regiao_metropolitana else 0,
        "idade_quadrado": idade_quadrado,
        "experiencia_aprox": experiencia_aprox,
        "idade_x_estudo": idade * anos_estudo,
        "estudo_x_horas": anos_estudo * horas_trabalhadas,
        "estudo_x_carteira": float(anos_estudo * carteira_flag),
        "idade_x_horas": idade * horas_trabalhadas,
    }

    return pd.DataFrame([features])


def _map_regiao(sigla_uf: str) -> str:
    norte = {"AC", "AM", "AP", "PA", "RO", "RR", "TO"}
    nordeste = {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"}
    sudeste = {"ES", "MG", "RJ", "SP"}
    sul = {"PR", "RS", "SC"}
    centro_oeste = {"DF", "GO", "MT", "MS"}

    if sigla_uf in norte:
        return "1"
    if sigla_uf in nordeste:
        return "2"
    if sigla_uf in sudeste:
        return "3"
    if sigla_uf in sul:
        return "4"
    if sigla_uf in centro_oeste:
        return "5"

    raise ValueError(f"UF invalida: {sigla_uf}")
