# ml_pipeline/src/config/settings.py
"""
Configurações globais do pipeline de dados e modelagem
Projeto: TCC Previsor de Renda

Atualizações (v2.1+):
- Flags de recorte por UF e urbano (para estratégias de segmentação)
- Suporte a modelos por segmento (ex.: ES urbano)
- Parâmetros para alvo log e correção via smearing (opcional)
"""

from pathlib import Path

# ======================================================
# PATHS DO PROJETO
# ======================================================

# Raiz do projeto (tcc-previsor-renda/)
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Diretórios de dados (NÃO versionados)
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_INTERIM_DIR = DATA_DIR / "interim"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

# Diretório de documentação
DOCS_DIR = PROJECT_ROOT / "docs"
DATA_CONTRACT_PATH = DOCS_DIR / "data_contract.md"

# Diretório de queries SQL
SQL_DIR = PROJECT_ROOT / "sql" / "bigquery"

# Garante que os diretórios existam
for _dir in [DATA_RAW_DIR, DATA_INTERIM_DIR, DATA_PROCESSED_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ======================================================
# BIGQUERY
# ======================================================

BQ_PROJECT_ID = "shining-rush-477809-m9"  # usa o projeto padrão autenticado (ADC)
BQ_DATA_PROJECT = "basedosdados"
BQ_DATASET_PNAD = "br_ibge_pnad"
BQ_TABLE_PESSOA = "microdados_compatibilizados_pessoa"
BQ_LOCATION = "US"

# ======================================================
# MAPA CONCEITUAL → COLUNAS TÉCNICAS (PNAD)
# ======================================================

PNAD_COLUMN_MAP = {
    # Capital humano
    "anos_estudo": "anos_estudo",
    "ultimo_grau_frequentado": "ultimo_grau_frequentado",
    "sabe_ler_escrever": "sabe_ler_escrever",

    # Experiência
    "idade": "idade",

    # Demografia
    "sexo": "sexo",
    "raca_cor": "raca_cor",

    # Trabalho
    "trabalhou_semana": "trabalhou_semana",
    "ocupacao_semana": "ocupacao_semana",
    "atividade_ramo_negocio_semana": "atividade_ramo_negocio_semana",
    "posicao_ocupacao": "posicao_ocupacao",
    "possui_carteira_assinada": "possui_carteira_assinada",
    "horas_trabalhadas_semana": "horas_trabalhadas_semana",

    # Geografia (nível pessoa)
    "sigla_uf": "sigla_uf",
    "regiao": "id_regiao",
}

# ======================================================
# FILTROS DO ESTUDO (DECISÕES METODOLÓGICAS)
# ======================================================

MIN_AGE = 18
FILTER_OCUPADOS = True
FILTER_TRABALHOU_SEMANA = True

# ======================================================
# AMOSTRAGEM
# ======================================================

SAMPLE_SIZE = 200_000
RANDOM_SEED = 42

# ======================================================
# VARIÁVEL ALVO
# ======================================================

TARGET_COLUMN = "renda_mensal_ocupacao_principal_deflacionado"
ALTERNATIVE_TARGET_COLUMN = "renda_mensal_todos_trabalhos_deflacionada"

# ======================================================
# SEGMENTAÇÃO / RECORTES (NOVO)
# ======================================================
# Objetivo: permitir treinar modelos específicos (ex.: ES urbano),
# sem espalhar "if sigla_uf == 'ES'" pelo código.

# Se True, filtra dataset para conter APENAS essas UFs (lista).
ENABLE_UF_FILTER = False
UF_WHITELIST = ["ES"]  # quando ENABLE_UF_FILTER=True

# Se True, filtra para zona urbana = 1.
ENABLE_URBAN_ONLY = False

# Colunas que representam urbano/metrópole (devem existir no dataset)
URBAN_COLUMN = "zona_urbana"
METRO_COLUMN = "regiao_metropolitana"
UF_COLUMN = "sigla_uf"

# “Segmentos” para experimentos (para salvar modelos/outputs com nomes consistentes)
# Ex.: "global", "es", "urban", "es_urban"
MODEL_SEGMENT_NAME = "global"

# ======================================================
# VARIÁVEIS EXPLICATIVAS (X)
# ======================================================

FEATURE_COLUMNS = [
    # Capital humano
    "anos_estudo",
    "ultimo_grau_frequentado",
    "sabe_ler_escrever",

    # Experiência / ciclo de vida
    "idade",

    # Demografia
    "sexo",
    "raca_cor",

    # Inserção no mercado de trabalho
    "trabalhou_semana",
    "ocupacao_semana",
    "atividade_ramo_negocio_semana",
    "posicao_ocupacao",
    "possui_carteira_assinada",
    "horas_trabalhadas_semana",

    # Contexto geográfico
    "sigla_uf",
    "regiao",

    # Contexto territorial (ativar se estiver no dataset)
    "zona_urbana",
    "regiao_metropolitana",
]

# ======================================================
# SPLIT TREINO / VAL / TESTE
# ======================================================

TRAIN_SIZE = 0.7
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15

STRATIFY_COLUMN = "faixa_renda"

# Coluna de grupo para evitar leakage domiciliar (quando aplicável)
GROUP_COLUMN = "id_domicilio"

# ======================================================
# TRANSFORMAÇÕES
# ======================================================

# Estratégia recomendada: modelar no log e corrigir com smearing (opcional)
APPLY_LOG_TARGET = True

# Se True, usa log1p para ser mais estável numericamente (recomendável)
USE_LOG1P = True

# Se True, aplica correção de smearing na volta do log para renda (opcional)
ENABLE_SMEARING = False

# Quantis usados para definir outliers
LOWER_INCOME_QUANTILE = 0.01
UPPER_INCOME_QUANTILE = 0.99

# ======================================================
# TREINO (HIPERPARÂMETROS PADRÃO / CONTROLES)
# ======================================================

# Early stopping padrão para boosting
EARLY_STOPPING_ROUNDS = 50

# Se você quiser rodar tuning depois, deixa ligado
ENABLE_TUNING = False