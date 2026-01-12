# Modelo Avançado — XGBoost  
**Projeto:** TCC Previsor de Renda  
**Dataset:** PNAD Contínua (IBGE / Base dos Dados)  
**Pipeline:** ml_pipeline  
**Data:** 12/01/2026  

---

## 1. Objetivo do Modelo XGBoost

O objetivo deste experimento foi avaliar o desempenho de um modelo de **gradient boosting baseado em árvores (XGBoost)** na predição da renda mensal do trabalho principal, comparando-o com os modelos previamente testados (**ElasticNet** e **HistGradientBoosting**).

Este modelo foi incluído com as seguintes finalidades:
- Testar um algoritmo reconhecido por alto desempenho em problemas tabulares;
- Avaliar a capacidade do modelo em capturar não linearidades e interações complexas;
- Comparar sua performance com modelos menos flexíveis;
- Analisar a interpretabilidade via SHAP.

---

## 2. Descrição do Modelo

### 2.1 Algoritmo
- **XGBoost Regressor (`XGBRegressor`)**
- Implementação baseada em gradient boosting com árvores de decisão

O XGBoost constrói um conjunto de árvores sequenciais, otimizadas via gradiente, com forte controle de regularização e estratégias avançadas de poda e amostragem.

---

### 2.2 Configuração Inicial

- `n_estimators = 500`
- `max_depth = 6`
- `learning_rate = 0.05`
- `subsample = 0.8`
- `colsample_bytree = 0.8`
- `random_state` fixo para reprodutibilidade

> Observação: os hiperparâmetros utilizados correspondem a uma configuração robusta inicial, **sem ajuste fino extensivo**.

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

### 4.2 Variáveis Categóricas (One-Hot Encoding)
- `sexo`
- `raca_cor`
- `trabalhou_semana`
- `ultimo_grau_frequentado`
- `posicao_ocupacao`
- `possui_carteira_assinada`
- `sigla_uf`
- `regiao`

> Colunas com potencial vazamento de alvo (ex.: versões log-transformadas da renda) foram removidas explicitamente antes do treino.

---

## 5. Pré-processamento

- Pipeline unificado com `ColumnTransformer`;
- Padronização (`StandardScaler`) para variáveis numéricas;
- Codificação One-Hot para variáveis categóricas;
- Tratamento automático de categorias desconhecidas no conjunto de teste.

A estrutura de pré-processamento foi mantida consistente com os modelos anteriores, garantindo comparabilidade direta.

---

## 6. Divisão dos Dados

| Conjunto | Registros |
|--------|-----------|
| Treino | ~2.344 |
| Validação | ~503 |
| Teste | ~503 |

- Divisão estratificada por faixas de renda;
- Separação idêntica à utilizada nos experimentos anteriores.

---

## 7. Métricas de Avaliação

### 7.1 Conjunto de Validação

| Métrica | Valor |
|------|------|
| RMSE | 2.846,04 |
| MAE | 1.725,79 |
| R² | 0,0598 |

---

### 7.2 Conjunto de Teste (Avaliação Final)

| Métrica | Valor |
|------|------|
| RMSE | 2.511,67 |
| MAE | 1.545,27 |
| R² | 0,1536 |

---

## 8. Análise dos Resultados

### 8.1 Desempenho Geral

O modelo XGBoost apresentou desempenho **inferior aos modelos previamente avaliados**, explicando aproximadamente **15% da variância da renda** no conjunto de teste.

Comparativamente:
- Teve desempenho inferior ao **HistGradientBoosting**;
- Não superou o **ElasticNet baseline** em termos de R²;
- Apresentou maior variabilidade nos erros.

Esse resultado indica que a maior flexibilidade do modelo **não se traduziu em melhor generalização** para este problema específico.

---

### 8.2 Interpretação Econômica

Apesar do desempenho limitado, o modelo aprendeu relações **economicamente coerentes**, incluindo:
- Retorno positivo da escolaridade (`anos_estudo`);
- Relação não linear da idade com a renda;
- Impacto positivo da carga horária semanal;
- Diferenças regionais e institucionais relevantes.

Esses padrões reforçam a consistência do pipeline e das variáveis utilizadas.

---

## 9. Análise de Interpretabilidade (SHAP)

A análise SHAP foi realizada utilizando abordagem **model-agnostic**, devido a limitações de compatibilidade entre o XGBoost encapsulado em `Pipeline` e o `TreeExplainer`.

---

### 9.1 Principais Variáveis Identificadas

- Escolaridade (`anos_estudo`);
- Idade;
- Horas trabalhadas por semana;
- Atividade econômica;
- Variáveis regionais (UF e região).

---

### 9.2 Observações Relevantes

- O gráfico SHAP apresentou **valores extremos de impacto**, indicando regras muito específicas;
- Evidência de **overfitting local**, com decisões baseadas em poucos exemplos;
- Fragmentação excessiva do impacto entre múltiplas variáveis dummy.

Esses padrões sugerem que o modelo ajustou **ruído em vez de estruturas gerais**.

---

## 10. Limitações do Modelo

- Sensibilidade elevada à esparsidade gerada pelo One-Hot Encoding;
- Tendência a sobreajuste em categorias pouco representadas;
- Dificuldade em generalizar relações socioeconômicas altamente ruidosas;
- Menor robustez em comparação com modelos de boosting mais restritivos.

---

## 11. Conclusão

Embora o XGBoost seja amplamente reconhecido como um modelo de alto desempenho em dados tabulares, **neste estudo ele não apresentou ganhos relevantes** em relação a modelos mais simples ou menos flexíveis.

Este resultado evidencia que:
- Maior complexidade não garante melhor desempenho;
- A natureza da variável renda impõe limites à modelagem;
- Modelos com maior regularização podem generalizar melhor neste contexto.

O XGBoost cumpriu seu papel como **experimento avançado comparativo**, mas **não foi selecionado como modelo final**.

---
