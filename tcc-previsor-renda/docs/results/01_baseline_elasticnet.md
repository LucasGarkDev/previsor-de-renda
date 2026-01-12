# Modelo Baseline — ElasticNet  
**Projeto:** TCC Previsor de Renda  
**Dataset:** PNAD Contínua (IBGE / Base dos Dados)  
**Pipeline:** ml_pipeline  
**Data:** 07/01/2026  

---

## 1. Objetivo do Modelo Baseline

O objetivo deste primeiro modelo foi estabelecer um **baseline estatístico** para a predição da renda mensal do trabalho principal, utilizando um modelo linear regularizado (**ElasticNet**).  

Este baseline tem como funções principais:
- Validar o pipeline completo de dados (extração → transformação → modelagem);
- Verificar a coerência estatística das variáveis explicativas;
- Servir como **ponto de comparação** para modelos mais avançados;
- Produzir evidências iniciais sobre os principais determinantes da renda.

---

## 2. Descrição do Modelo

### 2.1 Algoritmo
- **ElasticNet Regression**
- Combinação de:
  - Regularização L1 (Lasso)
  - Regularização L2 (Ridge)

### 2.2 Configuração
- `alpha = 1.0`
- `l1_ratio = 0.5`
- Otimização padrão do scikit-learn
- Seed fixa para reprodutibilidade

### 2.3 Justificativa da escolha
O ElasticNet foi escolhido por:
- Ser interpretável;
- Lidar com multicolinearidade;
- Fornecer um baseline robusto e simples;
- Facilitar a comparação com modelos não lineares posteriores.

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

### 4.2 Variáveis Categóricas (One-Hot Encoding)
- `sexo`
- `raca_cor`
- `trabalhou_semana`
- `ultimo_grau_frequentado`
- `posicao_ocupacao`
- `possui_carteira_assinada`
- `sigla_uf`
- `regiao`

> Observação: colunas com potencial vazamento de alvo (ex.: versões log-transformadas da renda) foram removidas explicitamente antes do treino.

---

## 5. Pré-processamento

- Padronização (`StandardScaler`) para variáveis numéricas;
- Codificação One-Hot para variáveis categóricas;
- Pipeline unificado com `ColumnTransformer`;
- Tratamento implícito de categorias desconhecidas no conjunto de validação/teste.

---

## 6. Divisão dos Dados

| Conjunto | Registros |
|-------|----------|
| Treino | 2.344 |
| Validação | 503 |
| Teste | 503 |

- Divisão estratificada por faixas de renda;
- Garantia de representatividade entre os conjuntos.

---

## 7. Métricas de Avaliação

### 7.1 Conjunto de Validação

| Métrica | Valor |
|------|------|
| RMSE | 2.672,01 |
| MAE | 1.641,91 |
| R² | 0,1713 |

---

### 7.2 Conjunto de Teste (Avaliação Final)

| Métrica | Valor |
|------|------|
| RMSE | 2.471,84 |
| MAE | 1.573,68 |
| R² | 0,1802 |

---

## 8. Análise dos Resultados

### 8.1 Desempenho Geral
O modelo apresentou desempenho **moderado**, explicando aproximadamente **18% da variância** da renda no conjunto de teste.  

Esse resultado é compatível com:
- A natureza altamente heterogênea da renda;
- A presença de relações não lineares e interações complexas;
- As limitações intrínsecas de modelos lineares para esse tipo de problema.

---

### 8.2 Coerência Econômica
Apesar do desempenho limitado, o modelo capturou relações economicamente consistentes:
- Retorno positivo da escolaridade;
- Aumento da renda com maior carga horária;
- Perfil etário com efeito não linear;
- Diferenças regionais e institucionais (UF e região).

Esses padrões foram confirmados posteriormente por análise SHAP.

---

## 9. Análise de Interpretabilidade (SHAP)

A análise SHAP indicou como variáveis mais relevantes:
1. `anos_estudo`
2. `horas_trabalhadas_semana`
3. `idade`
4. Variáveis regionais (`regiao`, `sigla_uf`)
5. Componentes categóricos de escolaridade e raça/cor

O gráfico SHAP evidenciou:
- Relações monotônicas positivas esperadas;
- Efeitos não lineares claros (especialmente idade);
- Fragmentação do impacto regional em múltiplas dummies.

---

## 10. Limitações do Modelo

- Incapacidade de capturar interações complexas;
- Sensibilidade a ruído categórico;
- Baixa flexibilidade para padrões não lineares;
- Performance limitada em comparação com modelos baseados em árvores.

---

## 11. Conclusão e Próximos Passos

O ElasticNet cumpriu seu papel como **modelo baseline**, validando o pipeline e fornecendo uma referência sólida para comparação.

Com base nos resultados e na análise SHAP, os próximos passos definidos são:
- Substituir o modelo por um algoritmo não linear (HistGradientBoostingRegressor);
- Aplicar engenharia de atributos guiada por interpretabilidade;
- Comparar formalmente os ganhos de desempenho.

Este baseline será mantido como referência fixa ao longo do projeto.

---
