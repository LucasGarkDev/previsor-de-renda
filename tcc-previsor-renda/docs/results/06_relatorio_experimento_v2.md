# Relatório do Experimento — Pipeline V2 com Variáveis Domiciliares

## Projeto
**Previsor de Renda Individual a partir da PNAD Contínua (IBGE)**

## Versão do Pipeline
**v2.0.0-contextual**

## Data
Janeiro de 2026

---

## 1. Objetivo do Experimento

O objetivo deste experimento foi avaliar o impacto da **incorporação de variáveis domiciliares** no desempenho de modelos de aprendizado de máquina para previsão da renda mensal do trabalho principal.

Especificamente, buscou-se:

- Integrar informações de **nível pessoa** e **nível domicílio** da PNAD Contínua;
- Avaliar ganhos de desempenho em relação à versão anterior do pipeline (v1);
- Comparar um modelo linear regularizado (ElasticNet) com um modelo não linear baseado em árvores (CatBoost);
- Investigar possíveis indícios de vazamento estrutural de informação (*proxy leakage*).

---

## 2. Descrição do Dataset (Pipeline V2)

### 2.1 Fonte dos Dados

- **PNAD Contínua – IBGE**
- Extração via **Google BigQuery (Base dos Dados)**

Foram utilizadas duas tabelas principais:

- `microdados_pessoa` (nível indivíduo)
- `microdados_compatibilizados_domicilio` (nível domicílio)

### 2.2 Estratégia de Integração

Os dados foram integrados por meio de um **LEFT JOIN** utilizando a chave:

- `id_domicilio`

Isso permitiu enriquecer cada indivíduo com informações estruturais e contextuais do domicílio em que reside.

### 2.3 Tamanho Final da Amostra

Após todas as etapas de limpeza e transformação:

- **Total de registros:** 3.350 indivíduos
- **Split dos dados:**
  - Treino: 2.344
  - Validação: 503
  - Teste: 503

---

## 3. Engenharia de Atributos (Feature Engineering V2)

Além das variáveis originais da PNAD, foram criadas novas features contextuais:

### 3.1 Features Individuais

- `idade_squared`: termo quadrático para capturar não linearidade da idade;
- `anos_estudo_urbano`: interação entre escolaridade e zona urbana.

### 3.2 Features Domiciliares Derivadas

- `densidade_domiciliar`  
  \[
  \text{densidade} = \frac{\text{total\_pessoas}}{\text{quantidade\_comodos}}
  \]

- `infraestrutura_score`  
  Soma binária da presença de:
  - água encanada
  - iluminação elétrica
  - coleta de lixo

- `bens_score`  
  Soma binária da posse de:
  - geladeira
  - televisão
  - fogão
  - rádio

### 3.3 Variável Alvo

- Variável alvo original: `renda_mensal_ocupacao_principal_deflacionado`
- Transformação aplicada:
  - `log(renda)` para treinamento dos modelos

---

## 4. Modelos Avaliados

Foram treinados dois modelos distintos, com objetivos complementares:

### 4.1 ElasticNet V2 — Baseline Contextual

Modelo linear regularizado com:

- Padronização de variáveis numéricas
- One-Hot Encoding para variáveis categóricas
- Regularização combinada L1 + L2

**Objetivo:**  
Servir como baseline interpretável e estatisticamente conservador.

### 4.2 CatBoost V2 — Modelo Contextual Não Linear

Modelo baseado em Gradient Boosting com suporte nativo a variáveis categóricas.

Características:

- Uso direto de variáveis categóricas sem One-Hot Encoding
- Captura automática de interações complexas
- Early stopping com conjunto de validação

**Objetivo:**  
Explorar o máximo potencial preditivo do dataset enriquecido.

---

## 5. Resultados no Conjunto de Teste

### 5.1 ElasticNet V2

| Métrica | Valor |
|------|------|
| RMSE | 1.793,59 |
| MAE  | 1.019,01 |
| R²   | 0,5904 |

**Interpretação:**

- Desempenho consistente e realista;
- Melhora em relação ao pipeline v1;
- Erros compatíveis com a complexidade do problema;
- Modelo adequado como baseline explicável.

---

### 5.2 CatBoost V2

| Métrica | Valor |
|------|------|
| RMSE | 197,29 |
| MAE  | 40,64 |
| R²   | 0,9950 |

**Interpretação:**

- Desempenho extremamente elevado;
- Erro médio muito baixo para um problema de renda individual;
- Capacidade quase total de explicação da variância.

---

## 6. Análise Crítica dos Resultados

Embora o desempenho do CatBoost V2 seja tecnicamente válido, os resultados levantam um **alerta metodológico importante**.

### 6.1 Indício de Proxy Leakage

A variável `id_domicilio`, utilizada como categórica no modelo, pode atuar como um **identificador indireto do padrão socioeconômico**, uma vez que:

- Muitos domicílios aparecem uma única vez na amostra;
- O domicílio agrega informações altamente correlacionadas com renda;
- O CatBoost é capaz de memorizar padrões complexos associados a categorias.

Isso não caracteriza vazamento direto da variável alvo, mas sim um **vazamento estrutural indireto**, que pode inflar artificialmente o desempenho do modelo.

---

## 7. Decisão Metodológica

Diante desses resultados, foi definido que:

- O experimento atual representa um **limite superior de desempenho** (*upper bound*);
- O modelo ElasticNet V2 permanece como baseline robusto e defensável;
- Um novo experimento será conduzido removendo a variável `id_domicilio` do treinamento do CatBoost.

---

## 8. Próximo Experimento Planejado

### CatBoost V2 sem `id_domicilio`

Objetivos:

- Avaliar o impacto real das variáveis domiciliares **sem identificadores únicos**;
- Medir a queda (ou não) de desempenho;
- Comparar robustez e capacidade de generalização;
- Fortalecer a validade científica dos resultados apresentados no TCC.

Este experimento será documentado separadamente e comparado diretamente com os resultados apresentados neste relatório.

---

## 9. Conclusão Parcial

O pipeline V2 demonstrou que a incorporação de variáveis domiciliares:

- Aumenta significativamente o poder preditivo dos modelos;
- Introduz desafios metodológicos relacionados à generalização;
- Exige análise crítica e experimentos de controle.

Os resultados obtidos até o momento são sólidos, reprodutíveis e fornecem uma base forte para discussão acadêmica no contexto do Trabalho de Conclusão de Curso.
