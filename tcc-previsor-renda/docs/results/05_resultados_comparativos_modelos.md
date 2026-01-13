# Comparação de Modelos e Resultados Finais  
**Projeto:** TCC Previsor de Renda  
**Dataset:** PNAD Contínua (IBGE / Base dos Dados)  
**Pipeline:** ml_pipeline  
**Data:** 13/01/2026  

---

## 1. Introdução

Este capítulo apresenta a **comparação final entre os modelos de Machine Learning avaliados** para a predição da renda mensal do trabalho principal.  

Após a construção de um pipeline completo, reprodutível e modular, foram testados modelos de diferentes naturezas — lineares, baseados em árvores e boosting — com o objetivo de avaliar desempenho preditivo, robustez e coerência econômica.

O foco desta etapa não é apenas identificar o modelo com melhor métrica, mas **avaliar o equilíbrio entre desempenho, estabilidade e interpretabilidade**, critérios fundamentais para aplicações socioeconômicas.

---

## 2. Modelos Avaliados

Os seguintes modelos foram treinados e avaliados no pipeline:

1. **ElasticNet**  
   - Modelo linear regularizado  
   - Utilizado como baseline estatístico  

2. **HistGradientBoostingRegressor**  
   - Modelo não linear baseado em árvores  
   - Captura interações e não linearidades  

3. **XGBoost Regressor**  
   - Modelo avançado de gradient boosting  
   - Alta flexibilidade, maior risco de overfitting  

4. **CatBoost Regressor**  
   - Boosting com tratamento nativo de variáveis categóricas  
   - Reduz esparsidade e fragmentação de efeitos  

Todos os modelos foram avaliados utilizando o **mesmo conjunto de teste**, garantindo comparabilidade direta.

---

## 3. Métricas de Avaliação

As métricas utilizadas foram:

- **RMSE (Root Mean Squared Error)**  
- **MAE (Mean Absolute Error)**  
- **R² (Coeficiente de Determinação)**  

Essas métricas permitem avaliar tanto o erro médio quanto a capacidade explicativa global do modelo.

---

## 4. Tabela Comparativa Final (Conjunto de Teste)

| Modelo | RMSE | MAE | R² |
|------|------|------|----|
| ElasticNet | 2.471,84 | 1.573,68 | 0,1802 |
| HistGradientBoosting | **2.420,11** | **1.503,42** | 0,2140 |
| XGBoost | 2.512,33 | 1.545,02 | 0,1541 |
| **CatBoost** | 2.386,92 | 1.471,60 | **0,2356** |

> Observação: valores apresentados referem-se ao conjunto de teste, utilizado exclusivamente para avaliação final.

---

## 5. Análise Comparativa dos Resultados

### 5.1 ElasticNet (Baseline)

O ElasticNet apresentou desempenho moderado, explicando cerca de **18% da variância da renda**.  
Apesar de limitado pela linearidade, cumpriu adequadamente seu papel como baseline, validando o pipeline e fornecendo referência inicial.

---

### 5.2 HistGradientBoosting

O HistGradientBoosting apresentou melhora significativa em relação ao baseline linear, capturando relações não lineares e interações entre variáveis.  

- Desempenho consistente  
- Boa estabilidade  
- SHAP revelou padrões economicamente coerentes  

Este modelo tornou-se a **primeira referência não linear sólida** do projeto.

---

### 5.3 XGBoost

Apesar de sua capacidade expressiva, o XGBoost apresentou desempenho inferior ao HistGradientBoosting e ao CatBoost no conjunto de teste.

A análise SHAP indicou:
- Impactos extremos em algumas variáveis
- Fragmentação excessiva causada pelo One-Hot Encoding
- Indícios de overfitting local

Dessa forma, o modelo não generalizou melhor, apesar de sua complexidade.

---

### 5.4 CatBoost (Modelo Final)

O CatBoost apresentou o **melhor desempenho geral** entre os modelos avaliados:

- Maior R² no conjunto de teste
- Menor MAE
- Boa estabilidade
- Interpretação consistente via SHAP

O tratamento nativo de variáveis categóricas permitiu:
- Redução da esparsidade
- Efeitos categóricos mais suaves
- Melhor generalização

---

## 6. Ajuste Leve de Hiperparâmetros (Tuning)

Foi realizado um ajuste leve de hiperparâmetros no CatBoost, avaliando variações de:
- Profundidade das árvores (`depth`)
- Taxa de aprendizado (`learning_rate`)

Os resultados no conjunto de validação indicaram **variações marginais nas métricas**, sem ganhos consistentes em relação à configuração inicial.

Esse comportamento sugere que o modelo original **já se encontrava próximo do ponto ótimo**, reforçando sua robustez e reduzindo o risco de overfitting por tuning excessivo.

---

## 7. Interpretabilidade e Coerência Econômica

A análise SHAP do modelo CatBoost confirmou padrões esperados na literatura econômica:

- Retorno positivo da escolaridade
- Efeito não linear da idade
- Impacto da carga horária semanal
- Diferenças regionais e institucionais
- Importância do vínculo formal de trabalho

Esses resultados reforçam que o modelo não apenas performa bem estatisticamente, mas também **aprende relações economicamente plausíveis**.

---

## 8. Limitações

Apesar do bom desempenho relativo, o modelo apresenta limitações inerentes ao problema:

- Renda é altamente heterogênea e influenciada por fatores não observados
- Ausência de variáveis latentes (habilidade, qualidade da firma, capital social)
- Dados transversais limitam a explicação da variância total

Valores de R² entre **0,20 e 0,30** são comuns em problemas desse tipo, especialmente em dados socioeconômicos individuais.

---

## 9. Conclusão

Com base nos resultados obtidos, o **CatBoost Regressor** foi selecionado como **modelo final do projeto**, por apresentar:

- Melhor desempenho preditivo no conjunto de teste
- Estabilidade frente a ajustes leves
- Alta interpretabilidade
- Coerência econômica dos padrões aprendidos

A etapa de modelagem é, portanto, considerada **encerrada**, permitindo o avanço para análises complementares e consolidação dos resultados no TCC.

---
