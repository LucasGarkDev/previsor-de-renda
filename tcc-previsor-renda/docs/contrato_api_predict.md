Aqui está o texto convertido integralmente para o formato **Markdown**, estruturado com a hierarquia correta de títulos, tabelas, blocos de código e formatação técnica.

---

# Contrato da API de Predição de Renda

**Projeto:** Previsor de Renda Individual – PNAD Contínua

**Modelo:** CatBoost V2 (sem `id_domicilio`)

**Endpoint:** `POST /predict`

---

## 1. Objetivo do Endpoint

O endpoint `/predict` tem como objetivo estimar a renda mensal esperada do trabalho principal de um indivíduo, a partir de características socioeconômicas, educacionais, ocupacionais e domiciliares, informadas de forma conceitual pelo usuário final.

**O backend é responsável por:**

* Validar os dados de entrada;
* Converter categorias conceituais em códigos utilizados no treinamento;
* Calcular métricas derivadas e scores agregados;
* Montar o vetor final de features esperado pelo modelo;
* Executar a predição via CatBoost.

---

## 2. Princípios de Projeto

* ❌ **O frontend não envia:** features derivadas, códigos PNAD ou variáveis de renda.
* ✅ **O backend centraliza:** toda a lógica de transformação.
* ✅ **O contrato é estável:** documentado e defensável metodologicamente.

---

## 3. Variáveis de Entrada (Contrato Conceitual)

### 3.1 Perfil Demográfico e Educacional

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `idade` | `int` | Idade do indivíduo |
| `anos_estudo` | `int` | Anos completos de estudo (0–17) |
| `ultimo_grau_frequentado` | `string` | Grau mais alto frequentado |
| `sabe_ler_escrever` | `bool` | Alfabetização |
| `sexo` | `string` | masculino ou feminino |
| `raca_cor` | `string` | branca, preta, parda, amarela, indigena |

### 3.2 Condição de Trabalho

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `trabalhou_semana` | `bool` | Trabalhou na semana de referência |
| `horas_trabalhadas_semana` | `int` | Horas trabalhadas |
| `ocupacao_semana` | `bool` | Está ocupado |
| `atividade_ramo_negocio_semana` | `int` | Código do setor de atividade |
| `posicao_ocupacao` | `string` | Posição na ocupação |
| `possui_carteira_assinada` | `bool` | Carteira assinada |

### 3.3 Localização

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `sigla_uf` | `string` | UF de residência |
| `zona_urbana` | `bool` | Reside em área urbana |
| `regiao_metropolitana` | `bool` | Região metropolitana |

> ⚠️ **Nota:** A variável `regiao` é derivada no backend a partir da UF.

### 3.4 Características do Domicílio

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `total_pessoas` | `int` | Pessoas no domicílio |
| `quantidade_comodos` | `int` | Total de cômodos |
| `quantidade_dormitorios` | `int` | Dormitórios |
| `possui_agua_rede` | `bool` | Água encanada |
| `tipo_esgoto` | `string` | Tipo de esgotamento |
| `lixo_coletado` | `bool` | Coleta de lixo |
| `possui_iluminacao_eletrica` | `bool` | Energia elétrica |
| `possui_geladeira` | `bool` | Geladeira |
| `possui_tv` | `bool` | Televisão |
| `possui_fogao` | `bool` | Fogão |
| `possui_radio` | `bool` | Rádio |

---

## 4. Variáveis Derivadas (Backend)

*Estas variáveis não são fornecidas pelo frontend.*

### 4.1 Transformações Matemáticas

* **idade_squared:** 
* **densidade_domiciliar:** 
* **anos_estudo_urbano:** 

### 4.2 Scores Agregados

* **Infraestrutura:** `infraestrutura_score = possui_agua_rede + possui_iluminacao_eletrica + (tipo_esgoto adequado ? 1 : 0)`
* **Bens Duráveis:** `bens_score = possui_geladeira + possui_tv + possui_fogao + possui_radio`

---

## 5. Variáveis Proibidas no Endpoint

Estas variáveis **nunca** podem ser enviadas ao `/predict`:

* `id_domicilio`
* `renda_mensal_ocupacao_principal_deflacionado`
* `log_renda_mensal_ocupacao_principal_deflacionado`

**Motivo:** vazamento de target (*proxy leakage*).

---

## 6. Schema Pydantic – Entrada (PredictInput)

```python
from pydantic import BaseModel, Field
from typing import Literal

class PredictInput(BaseModel):
    # Perfil demográfico
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

    # Trabalho
    trabalhou_semana: bool
    horas_trabalhadas_semana: int = Field(..., ge=0, le=100)
    ocupacao_semana: bool
    atividade_ramo_negocio_semana: int
    posicao_ocupacao: Literal["empregado", "empregador", "conta_propria", "outro"]
    possui_carteira_assinada: bool

    # Localização
    sigla_uf: str = Field(..., min_length=2, max_length=2)
    zona_urbana: bool
    regiao_metropolitana: bool

    # Domicílio
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

```

---

## 7. Schema de Saída (PredictOutput)

```python
class PredictOutput(BaseModel):
    renda_estimada: float = Field(..., description="Renda mensal estimada em reais")

```

---

## 8. Observação Metodológica (para o TCC)

O sistema implementa um pipeline de inferência explícito, no qual variáveis latentes e métricas derivadas são calculadas exclusivamente no backend, garantindo coerência com o processo de treinamento, evitando vazamento de informação e preservando a interpretabilidade do modelo.

---

Deseja que eu crie um exemplo de **requisição JSON** baseado neste contrato para testar sua API?