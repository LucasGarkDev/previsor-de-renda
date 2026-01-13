# Metodologia  
**Projeto:** Previsor de Renda  
**Dataset:** PNAD Contínua (IBGE / Base dos Dados)  

---

## 1. Visão Geral Metodológica

Este projeto tem como objetivo desenvolver um modelo de Machine Learning capaz de **prever a renda mensal do trabalho principal** de indivíduos ocupados, utilizando dados da **PNAD Contínua**, disponibilizados pela plataforma **Base dos Dados**.

A metodologia adotada combina:
- princípios de econometria aplicada;
- boas práticas de ciência de dados;
- técnicas modernas de aprendizado de máquina;
- forte ênfase em **interpretabilidade e coerência econômica**.

O foco do trabalho não é apenas maximizar métricas preditivas, mas construir um modelo **robusto, explicável e metodologicamente consistente**.

---

## 2. Fonte de Dados

Os dados utilizados provêm da tabela:

- `basedosdados.br_ibge_pnad.microdados_compatibilizados_pessoa`

Essa base contém informações individuais sobre características demográficas, educacionais, ocupacionais e geográficas dos respondentes da PNAD Contínua.

A extração e o tratamento inicial dos dados foram realizados de forma reprodutível, conforme documentado no `data_snapshot.md`.

---

## 3. Unidade de Análise

A **unidade de análise do modelo é o indivíduo ocupado**.

Cada observação corresponde a uma pessoa com idade igual ou superior a 18 anos que:
- declarou ter trabalhado na semana de referência;
- possui ocupação registrada;
- apresentou renda válida para o trabalho principal.

A variável alvo representa a **renda mensal do trabalho principal**, em valores deflacionados.

---

## 4. Variável Alvo

- **Target:** `renda_mensal_ocupacao_principal_deflacionado`
- Unidade: Reais (R$)
- Deflacionamento realizado conforme metodologia da Base dos Dados

A renda é tratada como uma variável contínua, altamente assimétrica e influenciada por múltiplos fatores observáveis e não observáveis.

---

## 5. Escopo das Variáveis Explicativas

### 5.1 Dimensões consideradas

Nesta etapa do projeto, as variáveis explicativas foram organizadas nas seguintes dimensões:

- **Capital humano:** escolaridade e alfabetização;
- **Experiência e ciclo de vida:** idade e transformações não lineares;
- **Demografia:** sexo e raça/cor;
- **Inserção no mercado de trabalho:** ocupação, setor, posição na ocupação, formalização e carga horária;
- **Contexto geográfico:** UF e região.

Essas variáveis permitem capturar os principais determinantes individuais da renda descritos na literatura econômica.

---

### 5.2 Variáveis excluídas deliberadamente

Optou-se por **não incluir**, nesta fase:

- renda domiciliar como variável explicativa;
- bens duráveis do domicílio;
- transferências sociais;
- agregações de renda de outros moradores.

Essa decisão metodológica visa:
- evitar vazamento direto ou indireto da variável alvo;
- preservar a interpretabilidade econômica do modelo;
- avaliar a capacidade preditiva baseada predominantemente em características individuais e ocupacionais.

Reconhece-se que essas exclusões impõem um limite explicativo ao modelo, o que é considerado e discutido nos resultados.

---

## 6. Pré-processamento dos Dados

As etapas de pré-processamento incluem:

- remoção explícita de variáveis com potencial vazamento de alvo;
- tratamento de valores ausentes;
- transformação de variáveis quando necessário (ex.: termos quadráticos);
- padronização ou codificação apenas quando exigido pelo modelo.

Para modelos baseados em árvores com tratamento nativo de categóricas (CatBoost), as variáveis categóricas foram mantidas em formato original, com valores ausentes tratados como categoria explícita.

---

## 7. Divisão dos Dados

O conjunto de dados foi dividido em três subconjuntos:

| Conjunto | Proporção |
|--------|----------|
| Treino | ~70% |
| Validação | ~15% |
| Teste | ~15% |

A divisão foi realizada de forma **estratificada por faixas de renda**, garantindo representatividade e comparabilidade entre os conjuntos.

O conjunto de teste foi reservado exclusivamente para a avaliação final dos modelos.

---

## 8. Pipeline de Machine Learning

O projeto foi estruturado como um **pipeline modular**, composto pelas seguintes etapas:

1. Extração e filtragem dos dados;
2. Engenharia de atributos;
3. Divisão dos dados;
4. Treinamento de múltiplos modelos;
5. Avaliação quantitativa;
6. Análise de interpretabilidade (SHAP);
7. Exportação de modelos e métricas;
8. Documentação dos resultados.

Essa organização garante:
- reprodutibilidade;
- facilidade de manutenção;
- extensibilidade para novos experimentos.

---

## 9. Modelos Avaliados

Foram avaliados modelos de diferentes naturezas:

- **ElasticNet** (baseline linear);
- **HistGradientBoostingRegressor** (baseline não linear);
- **XGBoost Regressor** (modelo avançado baseado em One-Hot Encoding);
- **CatBoost Regressor** (boosting com tratamento nativo de categóricas).

A comparação entre modelos permitiu avaliar ganhos incrementais de complexidade e seus impactos no desempenho e na interpretabilidade.

---

## 10. Métricas de Avaliação

As métricas utilizadas foram:

- **RMSE (Root Mean Squared Error):** penaliza erros grandes;
- **MAE (Mean Absolute Error):** mede erro médio absoluto;
- **R² (Coeficiente de Determinação):** avalia poder explicativo global.

Essas métricas foram analisadas em conjunto, evitando decisões baseadas em um único critério.

---

## 11. Interpretabilidade

A interpretabilidade dos modelos foi analisada por meio de **SHAP (SHapley Additive exPlanations)**.

Essa abordagem permitiu:
- identificar variáveis mais relevantes;
- analisar efeitos marginais;
- verificar coerência econômica dos padrões aprendidos;
- comparar estabilidade das explicações entre modelos.

A interpretabilidade foi tratada como critério central de decisão, e não como etapa acessória.

---

## 12. Ajuste de Hiperparâmetros

Para o modelo selecionado (CatBoost), foi realizado um **ajuste leve de hiperparâmetros**, avaliando pequenas variações de profundidade e taxa de aprendizado.

Os resultados indicaram ganhos marginais, sugerindo que a configuração inicial já se encontrava próxima do ótimo, evitando tuning excessivo e risco de overfitting.

---

## 13. Limitações Metodológicas

As principais limitações reconhecidas são:

- natureza transversal dos dados;
- ausência de variáveis latentes (habilidade, qualidade da firma, capital social);
- elevada heterogeneidade da renda individual;
- escopo deliberadamente restrito a variáveis individuais nesta fase.

Valores moderados de R² são esperados e compatíveis com a literatura para esse tipo de problema.

---

## 14. Considerações Finais

A metodologia adotada prioriza rigor, transparência e coerência econômica.  
As decisões de escopo e modelagem foram tomadas de forma consciente e documentadas, permitindo tanto a interpretação adequada dos resultados quanto a extensão futura do trabalho.

A etapa de modelagem é considerada metodologicamente encerrada, abrindo espaço para análises complementares e consolidação dos resultados no TCC.

---
