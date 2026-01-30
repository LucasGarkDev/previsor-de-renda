import pandas as pd
from backend.app.schemas.predict import PredictInput

# ============================
# Mapeamentos categóricos
# ============================

SEXO_MAP = {
    "masculino": "1",
    "feminino": "0",
}

RACA_COR_MAP = {
    "branca": "2",
    "preta": "4",
    "parda": "6",
    "amarela": "8",
    "indigena": "8",  # PNAD agrupa indígena/ignorado em alguns casos
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

TIPO_ESGOTO_MAP = {
    "rede": "2",
    "fossa": "4",
    "outro": "6",
    "nao_informado": "NA_DOM",
}


# ============================
# Função principal
# ============================

def build_model_features(data: PredictInput) -> pd.DataFrame:
    """
    Constrói o DataFrame de features exatamente no formato
    esperado pelo modelo CatBoost.
    """

    # ---------------------------
    # Variáveis diretas
    # ---------------------------
    idade = data.idade
    anos_estudo = data.anos_estudo

    # ---------------------------
    # Variáveis derivadas
    # ---------------------------
    idade_squared = idade ** 2
    densidade_domiciliar = data.total_pessoas / data.quantidade_comodos
    anos_estudo_urbano = anos_estudo * int(data.zona_urbana)

    # ---------------------------
    # Scores agregados
    # ---------------------------
    infraestrutura_score = (
        int(data.possui_agua_rede)
        + int(data.possui_iluminacao_eletrica)
        + (1 if data.tipo_esgoto == "rede" else 0)
    )

    bens_score = (
        int(data.possui_geladeira)
        + int(data.possui_tv)
        + int(data.possui_fogao)
        + int(data.possui_radio)
    )

    # ---------------------------
    # Montagem do vetor final
    # Ordem CRÍTICA: igual ao treino
    # ---------------------------
    features = {
        "anos_estudo": anos_estudo,
        "ultimo_grau_frequentado": data.ultimo_grau_frequentado,
        "sabe_ler_escrever": str(data.sabe_ler_escrever),
        "idade": idade,
        "sexo": data.sexo,
        "raca_cor": RACA_COR_MAP[data.raca_cor],
        "trabalhou_semana": "1" if data.trabalhou_semana else "0",
        "ocupacao_semana": 1 if data.ocupacao_semana else 0,
        "atividade_ramo_negocio_semana": data.atividade_ramo_negocio_semana,
        "posicao_ocupacao": POSICAO_OCUPACAO_MAP[data.posicao_ocupacao],
        "possui_carteira_assinada": "1" if data.possui_carteira_assinada else "NA_DOM",
        "horas_trabalhadas_semana": data.horas_trabalhadas_semana,
        "sigla_uf": data.sigla_uf,
        "regiao": _map_regiao(data.sigla_uf),
        "possui_agua_rede": int(data.possui_agua_rede),
        "tipo_esgoto": TIPO_ESGOTO_MAP[data.tipo_esgoto],
        "lixo_coletado": "1" if data.lixo_coletado else "NA_DOM",
        "possui_iluminacao_eletrica": int(data.possui_iluminacao_eletrica),
        "possui_geladeira": int(data.possui_geladeira),
        "possui_tv": int(data.possui_tv),
        "possui_fogao": int(data.possui_fogao),
        "possui_radio": int(data.possui_radio),
        "total_pessoas": data.total_pessoas,
        "quantidade_comodos": data.quantidade_comodos,
        "quantidade_dormitorios": data.quantidade_dormitorios,
        "zona_urbana": int(data.zona_urbana),
        "regiao_metropolitana": int(data.regiao_metropolitana),
        "idade_squared": idade_squared,
        "densidade_domiciliar": densidade_domiciliar,
        "infraestrutura_score": infraestrutura_score,
        "bens_score": bens_score,
        "anos_estudo_urbano": anos_estudo_urbano,
    }

    return pd.DataFrame([features])


# ============================
# Função auxiliar
# ============================

def _map_regiao(sigla_uf: str) -> str:
    NORTE = {"AC", "AM", "AP", "PA", "RO", "RR", "TO"}
    NORDESTE = {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"}
    SUDESTE = {"ES", "MG", "RJ", "SP"}
    SUL = {"PR", "RS", "SC"}
    CENTRO_OESTE = {"DF", "GO", "MT", "MS"}

    if sigla_uf in NORTE:
        return "1"
    if sigla_uf in NORDESTE:
        return "2"
    if sigla_uf in SUDESTE:
        return "3"
    if sigla_uf in SUL:
        return "4"
    if sigla_uf in CENTRO_OESTE:
        return "5"

    raise ValueError(f"UF inválida: {sigla_uf}")
