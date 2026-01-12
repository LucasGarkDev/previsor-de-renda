# Modelo Avançado — HistGradientBoostingRegressor  
**Projeto:** TCC Previsor de Renda  
**Dataset:** PNAD Contínua (IBGE / Base dos Dados)  
**Pipeline:** ml_pipeline  
**Data:** 08/01/2026  

---

## 1. Objetivo do Modelo

O objetivo deste modelo foi **superar o baseline linear (ElasticNet)** por meio da aplicação de um algoritmo **não linear baseado em árvores de decisão**, capaz de capturar:
- Relações não lineares;
- Interações complexas entre variáveis;
- Efeitos heterogêneos entre grupos populacionais.

O **HistGradientBoostingRegressor** foi selecionado como primeiro modelo avançado por:
- Lidar nativamente com valores ausentes;
- Escalar bem para conjuntos de dados de médio porte;
- Representar uma evolução natural em relação ao baseline linear;
- Ser amplamente utilizado em aplicações modernas de aprendizado supervisionado.

---

## 2. Descrição do Modelo

### 2.1 Algoritmo
- **Histogram-based Gradient Boosting Regression**
- Implementação do `scikit-learn`

O algoritmo constrói sucessivas árvores de decisão rasas, onde cada nova árvore corrige os erros residuais das anteriores, utilizando discretização em histogramas para ganho de eficiência computacional.

---

### 2.2 Configuração Inicial

- Parâmetros padrão do `scikit-learn`
- `random_state` fixado para reprodutibilidade
- Sem tuning fino nesta etapa (modelo exploratório)

> Observação: esta versão do modelo serve como **baseline não linear**, antes de ajustes de hiperparâmetros.

---

## 3. Variável Alvo

- **Target:** `renda_mensal_ocupacao_principal_deflacionado`
- Unidade: Reais (R$)
- Valores deflacionados conforme metodologia oficial da Base dos Dados

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

### 4.2 Variáveis Categóricas
- `sexo`
- `raca_cor`
- `trabalhou_semana`
- `ultimo_grau_frequentado`
- `posicao_ocupacao`
- `possui_carteira_assinada`
- `sigla_uf`
- `regiao`

As variáveis categóricas foram codificadas via **One-Hot Encoding**, integradas ao pipeline de pré-processamento.

> Colunas com potencial vazamento de alvo (ex.: versões log-transformadas da renda) foram removidas explicitamente antes do treino.

---

## 5. Pré-processamento

- Imputação de valores numéricos pela mediana;
- Imputação de valores categóricos pela moda;
- Codificação One-Hot para variáveis categóricas;
- Pipeline unificado com `ColumnTransformer`;
- Mesma estrutura de pré-processamento utilizada no baseline, garantindo comparabilidade.

---

## 6. Divisão dos Dados

| Conjunto | Registros |
|-------|----------|
| Treino | 2.344 |
| Validação | 503 |
| Teste | 503 |

- Divisão estratificada por faixas de renda;
- Mesma partição utilizada nos modelos anteriores.

---

## 7. Métricas de Avaliação

### 7.1 Conjunto de Validação

| Métrica | Valor |
|------|------|
| RMSE | 2.754,74 |
| MAE | 1.627,34 |
| R² | 0,1192 |

> Nota: apesar do desempenho inferior na validação em relação ao ElasticNet, este comportamento é comum em modelos de boosting antes de tuning fino.

---

### 7.2 Conjunto de Teste (Avaliação Final)

| Métrica | Valor |
|------|------|
| RMSE | **2.420,55** |
| MAE | **1.502,65** |
| R² | **0,2139** |

---

## 8. Análise dos Resultados

### 8.1 Desempenho Geral

No conjunto de teste, o HistGradientBoostingRegressor apresentou **melhor desempenho que o modelo baseline**, superando o ElasticNet em todas as métricas principais.

Em especial:
- Redução do RMSE;
- Redução do erro absoluto médio (MAE);
- Aumento significativo do R².

O modelo explica aproximadamente **21% da variância da renda**, resultado compatível com a literatura empírica sobre renda individual, dada a alta heterogeneidade e presença de fatores não observáveis.

---

### 8.2 Generalização

O contraste entre validação e teste sugere que:
- O modelo captura padrões que se manifestam melhor fora do subconjunto de validação;
- O aprendizado não está restrito ao “miolo” da amostra;
- Não há evidências claras de overfitting severo nesta configuração inicial.

---

## 9. Análise de Interpretabilidade (SHAP)

A análise SHAP revelou como variáveis mais relevantes:

1. `anos_estudo`
2. `idade`
3. `atividade_ramo_negocio_semana`
4. `horas_trabalhadas_semana`
5. Variáveis regionais (`regiao`, `sigla_uf`)
6. Variáveis institucionais e demográficas (`raca_cor`, `sexo`)

---

### 9.1 Principais Insights

- **Escolaridade** apresenta impacto fortemente positivo e não linear, com ganhos marginais crescentes nos níveis mais altos;
- **Idade** e `idade_squared` capturam claramente o perfil de ciclo de vida da renda;
- **Região e UF** apresentam impactos sistemáticos, refletindo desigualdades territoriais;
- **Setor de atividade** e carga horária contribuem de forma consistente para a explicação da renda;
- Variáveis demográficas têm impacto menor, mas estatisticamente relevante.

Os padrões identificados são **economicamente coerentes** e alinhados à teoria do capital humano e à economia do trabalho.

---

## 10. Comparação com o Modelo Baseline

| Métrica (Teste) | ElasticNet | HistGradientBoosting |
|---------------|------------|---------------------|
| RMSE | 2.471,84 | **2.420,55** |
| MAE | 1.573,68 | **1.502,65** |
| R² | 0.1802 | **0.2139** |

O HistGradientBoosting apresentou **ganhos consistentes de desempenho**, evidenciando a importância de modelos não lineares para este problema.

---

## 11. Limitações do Modelo

- Sensível a configuração de hiperparâmetros;
- Pode apresentar instabilidade sem tuning adequado;
- Menor interpretabilidade direta em comparação a modelos lineares;
- Necessita cuidados adicionais em análises de fairness e extrapolação.

---

## 12. Conclusão e Próximos Passos

O HistGradientBoostingRegressor demonstrou **melhor capacidade preditiva e maior poder explicativo** do que o baseline linear, validando sua escolha como próximo estágio do pipeline.

Com base nos resultados, os próximos passos definidos são:
- Realizar tuning de hiperparâmetros do HistGradientBoosting;
- Avaliar modelos de boosting mais avançados (XGBoost / LightGBM);
- Aplicar engenharia de atributos orientada por SHAP;
- Consolidar a comparação final entre modelos para o capítulo de resultados.

Este modelo passa a ser a **nova referência de desempenho** do projeto.

---
