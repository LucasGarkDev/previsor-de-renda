from pydantic import BaseModel, Field
from typing import Literal


class PredictInput(BaseModel):
    # ---------------------------
    # Perfil demográfico
    # ---------------------------
    idade: int = Field(..., ge=18, le=100)
    anos_estudo: int = Field(..., ge=0, le=17)
    ultimo_grau_frequentado: Literal[
        "fundamental_incompleto",
        "fundamental_completo",
        "medio_incompleto",
        "medio_completo",
        "superior_incompleto",
        "superior_completo"
    ]
    sabe_ler_escrever: bool
    sexo: Literal["masculino", "feminino"]
    raca_cor: Literal["branca", "preta", "parda", "amarela", "indigena"]

    # ---------------------------
    # Trabalho
    # ---------------------------
    trabalhou_semana: bool
    horas_trabalhadas_semana: int = Field(..., ge=0, le=100)
    ocupacao_semana: bool
    atividade_ramo_negocio_semana: int
    posicao_ocupacao: Literal[
        "empregado",
        "empregador",
        "conta_propria",
        "outro"
    ]
    possui_carteira_assinada: bool

    # ---------------------------
    # Localização
    # ---------------------------
    sigla_uf: str = Field(..., min_length=2, max_length=2)
    zona_urbana: bool
    regiao_metropolitana: bool

    # ---------------------------
    # Domicílio
    # ---------------------------
    total_pessoas: int = Field(..., ge=1)
    quantidade_comodos: int = Field(..., ge=1)
    quantidade_dormitorios: int = Field(..., ge=0)

    possui_agua_rede: bool
    tipo_esgoto: Literal["rede", "fossa", "outro", "nao_informado"]
    lixo_coletado: bool
    possui_iluminacao_eletrica: bool

    possui_geladeira: bool
    possui_tv: bool
    possui_fogao: bool
    possui_radio: bool


class PredictOutput(BaseModel):
    renda_estimada: float
