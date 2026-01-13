# Modelo Final — CatBoost Regressor  
**Projeto:** TCC Previsor de Renda  
**Dataset:** PNAD Contínua (IBGE / Base dos Dados)  
**Pipeline:** ml_pipeline  
**Data:** 13/01/2026  

---

## 1. Objetivo do Modelo

O objetivo deste modelo foi avaliar o desempenho do **CatBoost Regressor** como candidato a **modelo final** para a predição da renda mensal do trabalho principal, superando os modelos previamente testados (**ElasticNet**, **HistGradientBoosting** e **XGBoost**).

Este modelo foi incluído com as seguintes finalidades:
- Explorar um algoritmo de boosting com **tratamento nativo de variáveis categóricas**;
- Reduzir problemas de esparsidade introduzidos pelo One-Hot Encoding;
- Avaliar ganhos simultâneos de desempenho, robustez e interpretabilidade;
- Fundamentar a escolha do **modelo final do TCC** com base em evidência empírica.

---

## 2. Descrição do Modelo

### 2.1 Algoritmo
- **CatBoost Regressor**
- Algoritmo de gradient boosting baseado em árvores de decisão
- Implementação com *ordered boosting* e estatísticas alvo ordenadas

O CatBoost foi desenvolvido especificamente para lidar com:
- Variáveis categóricas de alta cardinalidade;
- Dados tabulares heterogêneos;
- Redução de overfitting em conjuntos com estrutura complexa.

---

### 2.2 Configuração Utilizada

- `iterations = 500`
- `depth = 8`
- `learning_rate = 0.05`
- `loss_function = RMSE`
- `eval_metric = RMSE`
- `random_seed` fixado para reprodutibilidade
- *Early stopping* com base no conjunto de validação

> Observação: foi utilizado um ajuste inicial robusto, sem tuning fino extensivo, priorizando estabilidade e comparabilidade com os demais modelos.

---

### 2.3 Justificativa da Escolha

O CatBoost foi escolhido por:
- Tratar variáveis categóricas de forma nativa, sem One-Hot Encoding;
- Reduzir fragmentação e esparsidade do espaço de atributos;
- Apresentar regularização implícita eficiente;
- Produzir explicações SHAP mais estáveis e coerentes;
- Ser amplamente adotado em problemas tabulares socioeconômicos.

---

## 3. Variável Alvo

- **Target:** `renda_mensal_ocupacao_principal_deflacionado`
- Unidade: Reais (R$)
- Valores deflacionados conforme metodologia da Base dos Dados

---

## 4. Variáveis Explicativas Utilizadas

### 4.1 Variáveis Numéricas
- `anos_estudo`
- `idade`
- `idade_squared`
- `horas_trabalhadas_semana`
- `ocupacao_semana`
- `atividade_ramo_negocio_semana`

---

### 4.2 Variáveis Categóricas (Tratamento Nativo)
- `sexo`
- `raca_cor`
- `trabalhou_semana`
- `ultimo_grau_frequentado`
- `sabe_ler_escrever`
- `posicao_ocupacao`
- `possui_carteira_assinada`
- `sigla_uf`
- `regiao`

> Observação: valores ausentes em variáveis categóricas foram tratados como uma categoria explícita (`"MISSING"`), conforme recomendado para modelos baseados em estatísticas ordenadas.

---

## 5. Pré-processamento

- Remoção explícita de colunas com potencial vazamento de alvo;
- Manutenção dos dados em formato tabular (`DataFrame`);
- Tratamento manual de valores ausentes em variáveis categóricas;
- Ausência de padronização ou codificação explícita, delegando o tratamento ao próprio modelo.

Essa abordagem garantiu **simetria entre treino, validação, teste e interpretabilidade**.

---

## 6. Divisão dos Dados

| Conjunto | Registros |
|-------|----------|
| Treino | 2.344 |
| Validação | 503 |
| Teste | 503 |

- Divisão estratificada por faixas de renda;
- Mesma partição utilizada nos modelos anteriores, garantindo comparabilidade direta.

---

## 7. Métricas de Avaliação

### 7.1 Conjunto de Teste (Avaliação Final)

| Métrica | Valor |
|------|------|
| RMSE | **2.386,92** |
| MAE | **1.471,60** |
| R² | **0.2356** |

---

## 8. Análise dos Resultados

### 8.1 Desempenho Geral

O CatBoost apresentou o **melhor desempenho entre todos os modelos avaliados**, superando:
- o baseline linear (ElasticNet);
- o baseline não linear (HistGradientBoosting);
- o modelo avançado baseado em One-Hot Encoding (XGBoost).

O modelo explica aproximadamente **23,6% da variância da renda** no conjunto de teste, resultado expressivo dada a elevada heterogeneidade e presença de fatores não observáveis associados à renda individual.

---

### 8.2 Comparação com Modelos Anteriores

| Modelo | RMSE | MAE | R² |
|------|------|-----|----|
| ElasticNet | 2.471,84 | 1.573,68 | 0.1802 |
| HistGradientBoosting | 2.420,55 | 1.502,65 | 0.2139 |
| XGBoost | 2.511,67 | 1.545,27 | 0.1536 |
| **CatBoost** | **2.386,92** | **1.471,60** | **0.2356** |

O CatBoost obteve ganhos consistentes em **todas as métricas**, indicando melhor equilíbrio entre flexibilidade e regularização.

---

## 9. Análise de Interpretabilidade (SHAP)

A interpretabilidade foi realizada utilizando o **TreeSHAP nativo do CatBoost**, abordagem mais adequada para modelos baseados em árvores com tratamento interno de variáveis categóricas.

---

### 9.1 Principais Variáveis Identificadas

As variáveis com maior impacto médio absoluto sobre a renda prevista foram:

1. `ultimo_grau_frequentado`
2. `regiao`
3. `anos_estudo`
4. `sigla_uf`
5. `raca_cor`
6. `sabe_ler_escrever`
7. `atividade_ramo_negocio_semana`
8. `horas_trabalhadas_semana`
9. `idade` e `idade_squared`

---

### 9.2 Principais Insights Econômicos

- **Escolaridade** apresenta impacto fortemente positivo e não linear, com retornos marginais maiores nos níveis mais altos;
- **Região e UF** capturam desigualdades territoriais estruturais;
- **Idade** reflete o padrão clássico de ciclo de vida da renda;
- **Carga horária e setor de atividade** contribuem de forma consistente;
- Variáveis demográficas apresentam impacto menor, porém sistemático.

Os efeitos estimados são **economicamente coerentes** e mais estáveis do que os observados em modelos com One-Hot Encoding.

---

## 10. Limitações do Modelo

- Parte significativa da variância da renda permanece não explicada, refletindo fatores não observáveis;
- O modelo não captura choques individuais ou eventos idiossincráticos;
- Resultados dependem da qualidade e granularidade das variáveis disponíveis na PNAD;
- Não foram exploradas extensões temporais ou regionais mais finas.

---

## 11. Conclusão

O CatBoost Regressor foi selecionado como **modelo final do TCC**, por apresentar:
- O melhor desempenho preditivo no conjunto de teste;
- Maior robustez frente a variáveis categóricas;
- Explicações SHAP mais estáveis e economicamente plausíveis;
- Adequação estrutural superior ao problema estudado.

Este modelo representa o melhor compromisso entre **precisão, interpretabilidade e coerência econômica**, atendendo plenamente aos objetivos do trabalho.

---
