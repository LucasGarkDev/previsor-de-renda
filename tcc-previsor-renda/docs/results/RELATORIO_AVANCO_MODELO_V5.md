# 📊 Relatório Técnico de Evolução do Modelo — Previsor de Renda (V5)

**Projeto:** TCC — Previsor de Renda com PNAD Contínua  
**Data:** 20/02/2026  
**Versão:** V5  
**Modelo:** CatBoost Regressor com Log-Target + Smearing Correction  

---

# 1️⃣ Contexto

O objetivo do projeto é desenvolver um modelo de Machine Learning capaz de estimar a renda mensal do indivíduo com base em variáveis sociodemográficas da PNAD Contínua.

Versões anteriores apresentavam limitações relacionadas a:

- Baixa amostragem
- Overfitting
- Instabilidade estatística
- Baixa capacidade explicativa

A versão V5 marca uma mudança estrutural significativa na metodologia.

---

# 2️⃣ Principais Estratégias Implementadas

## ✅ 2.1 Aumento da Amostra

- Extração via BigQuery com JOIN direto no ambiente da nuvem
- Sample inicial: 200.000 registros
- Após remoção de outliers: 172.003 registros
- Conjunto de treino final (v3): 120.402 registros

Impacto:
> Aumento expressivo de poder estatístico e redução de overfitting.

---

## ✅ 2.2 Transformação Logarítmica da Renda

A renda apresenta forte assimetria à direita.  
Foi aplicada transformação:

- `log1p(y)` ou `log(y)`
- Correção via **Smearing Correction**

Benefícios:

- Estabilização da variância
- Redução de impacto de outliers extremos
- Melhor generalização do modelo

---

## ✅ 2.3 Correção de Smearing

Aplicado fator de correção:
smearing_factor = mean(exp(residuals))


Objetivo:
Remover viés introduzido pela retransformação exponencial do log.

---

# 3️⃣ Resultados Obtidos

## 🔵 Modelo Global (V5)

| Métrica | Valor |
|----------|--------|
| Registros Treino | 120.402 |
| Registros Validação | 25.800 |
| RMSE | 919.24 |
| MAE | 476.00 |
| R² | **0.4559** |

---

## 🟢 Modelo Urbano (V5)

| Métrica | Valor |
|----------|--------|
| Registros Treino | 92.125 |
| Registros Validação | 19.850 |
| R² | **0.4573** |

Observação:
Segmentação urbano não trouxe ganho significativo em relação ao modelo global.

---

## 🟡 Modelo Espírito Santo (V5)

| Métrica | Valor |
|----------|--------|
| Registros Treino | 2.227 |
| Registros Validação | 462 |
| R² | **0.4000** |

Observação:
Segmentação por UF sofre com limitação de amostragem.

---

# 4️⃣ Análise Comparativa

| Estratégia | Resultado |
|-------------|------------|
| Aumento da amostra | ✅ Grande impacto positivo |
| Log-transform | ✅ Estabilização do modelo |
| Smearing Correction | ✅ Redução de viés |
| Segmentação Urbano | ❌ Ganho irrelevante |
| Segmentação por UF | ❌ Perda de poder estatístico |

---

# 5️⃣ Conclusões Técnicas

1. O aumento da base de dados foi a estratégia mais impactante.
2. O modelo global já internaliza efeitos urbanos como feature.
3. Segmentação explícita não demonstrou ganho relevante.
4. A limitação atual do modelo está mais relacionada à qualidade das features do que à arquitetura do algoritmo.

O modelo atual explica aproximadamente:

> 45% da variabilidade da renda mensal.

Considerando a natureza altamente complexa e multifatorial da renda, esse resultado é estatisticamente consistente.

---

# 6️⃣ Limitações Identificadas

- Variáveis não observáveis (capital social, networking, contexto regional fino)
- Ausência de variáveis macroeconômicas
- Falta de engenharia de interações estruturais
- Modelo ainda utiliza hiperparâmetros padrão

---

# 7️⃣ Próximos Passos Recomendados

## 🔹 Engenharia de Features

- Idade²
- Idade × Escolaridade
- Escolaridade ordinal
- Estimativa de experiência (idade - anos_estudo - 6)
- Agrupamento de ocupações

## 🔹 Teste com todos os anos disponíveis

## 🔹 Análise de Feature Importance
model.get_feature_importance(prettified=True)

## 🔹 Ajuste fino de hiperparâmetros

---

# 8️⃣ Conclusão Geral

A versão V5 representa um avanço metodológico significativo.

O projeto evoluiu de um modelo instável para uma estrutura estatisticamente robusta, com:

- Pipeline consolidado
- Segmentação testada empiricamente
- Estratégias comparadas com base quantitativa
- Evidência clara sobre impacto de volume de dados

O trabalho agora avança da fase exploratória para a fase de refinamento estrutural.

---

**Status Atual do Projeto:**  
Modelo funcional, validado e pronto para otimizações estruturais adicionais.