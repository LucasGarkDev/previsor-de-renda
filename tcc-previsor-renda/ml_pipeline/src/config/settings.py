"ml_pipeline/src/config/settings.py"

"""
Configurações globais do pipeline de dados e modelagem
Projeto: TCC Previsor de Renda
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

# Dataset principal definido no contrato de dados
BQ_PROJECT_ID = "shining-rush-477809-m9" # usa o projeto padrão autenticado (ADC)

# Projeto que CONTÉM os dados
BQ_DATA_PROJECT = "basedosdados"
BQ_DATASET_PNAD = "br_ibge_pnad"

# Tabela principal (nível pessoa)
BQ_TABLE_PESSOA = "microdados_compatibilizados_pessoa"

# Localização do BigQuery (default: US)
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

# Idade mínima considerada no estudo
MIN_AGE = 18

# Considerar apenas pessoas ocupadas
FILTER_OCUPADOS = True

# Considerar apenas quem trabalhou na semana de referência
FILTER_TRABALHOU_SEMANA = True

# ======================================================
# AMOSTRAGEM
# ======================================================

# Tamanho da amostra para desenvolvimento e treino
# (ajustável conforme a fase do projeto)
SAMPLE_SIZE = 200_000

# Seed global para reprodutibilidade
RANDOM_SEED = 42

# ======================================================
# VARIÁVEL ALVO
# ======================================================

TARGET_COLUMN = "renda_mensal_ocupacao_principal_deflacionado"

# Variável alternativa para análises de robustez
ALTERNATIVE_TARGET_COLUMN = "renda_mensal_todos_trabalhos_deflacionada"

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
    # "zona_urbana",
    # "regiao_metropolitana",
]

# ======================================================
# SPLIT TREINO / VAL / TESTE
# ======================================================

TRAIN_SIZE = 0.7
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15

# Coluna usada para estratificação (criada no pipeline)
STRATIFY_COLUMN = "faixa_renda"

# ======================================================
# TRANSFORMAÇÕES
# ======================================================

# Aplicar log na renda (para reduzir assimetria)
APPLY_LOG_TARGET = True

# Quantis usados para definir outliers
LOWER_INCOME_QUANTILE = 0.01
UPPER_INCOME_QUANTILE = 0.99
