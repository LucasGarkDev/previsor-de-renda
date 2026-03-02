# 📊 Relatório Técnico de Progresso

**Projeto:** Previsor de Renda — PNAD Contínua

**Versões:** V5 → V8

---

## 1. Contexto do Problema

O objetivo do projeto é desenvolver um modelo preditivo capaz de estimar a renda mensal do trabalho principal a partir de variáveis socioeconômicas da PNAD Contínua.

**Ferramentas e Métodos:**

* **Fonte:** Base dos Dados (BigQuery).
* **Algoritmo:** `CatBoost Regressor`.
* **Transformação:** Logarítmica do alvo ().
* **Métricas:** RMSE, MAE e .

> **Variável Alvo:** `renda_mensal_ocupacao_principal_deflacionado`

---

## 2. Evolução das Versões do Modelo

### 🔹 V5 — Estrutura Base Estável

* **Dataset:** v3 (200.000 amostras).
* **Tratamento:** Remoção de outliers (1% – 99%) e split estratificado.
* **Performance:** .

**Feature Importance (Top 5):**

| Variável | Importância |
| --- | --- |
| `anos_estudo` | ~26% |
| `horas_trabalhadas_semana` | ~10% |
| `idade` | ~9% |
| `sexo` | ~8% |
| `regiao` | ~7% |

---

### 🔹 V6 — Interações Não Lineares

Adição de features polinomiais e cruzadas: `idade_quadrado`, `experiencia_aprox`, `idade_x_estudo`.

* **Resultado:** .
* **Diagnóstico:** Ganho marginal pequeno. O CatBoost já captura não linearidades nativamente.

---

### 🔹 V7 — Interações Estruturais

Novas interações: `estudo_x_horas`, `estudo_x_carteira`, `idade_x_horas`.

* **Resultado:** .
* **Conclusão:** O modelo aproximou-se do limite estrutural para o conjunto atual de variáveis.

---

### 🔹 Tentativa de V8 — Multi-Ano

**Hipótese:** O limite do modelo estaria no uso de apenas um ano de dados.

* **Ação:** Investigação da tabela `microdados_compatibilizados_pessoa`.
* **Resultado:** A tabela **não possui** colunas temporais (ano/trimestre).
* **Conclusão:** O dataset já está consolidado; o gargalo não é a falta de dados temporais nesta tabela específica.

---

## 3. Diagnóstico Atual

📌 **O modelo já captura com precisão:**

* Capital humano (escolaridade), Intensidade de trabalho (horas), Experiência (idade), Formalidade (carteira) e Estrutura regional.

📌 **Estabilização do  em ~0.456:**
Isso sugere que o restante da variância depende de **fatores não observáveis** no dataset:

* Qualidade da ocupação e produtividade individual.
* Especificidades da empresa ou setor informal detalhado.
* Capital social e habilidades não medidas (soft skills).

---

## 4. Interpretação Econômica

O modelo é consistente com a **Literatura de Mincer**:



A dominância de `anos_estudo` (~26%) ratifica a **Teoria do Capital Humano** no cenário brasileiro.

---

## 5. Estado Atual do Modelo (Métricas)

| Métrica | Valor Aproximado |
| --- | --- |
| **RMSE** | ~918 |
| **MAE** | ~475 |
| **** | **~0.456** |

> **Status:** O modelo é estável, reprodutível e defensável academicamente.

---

## 6. Próximos Passos Estratégicos

A melhoria não virá de ajustes simples ou mais dados brutos, mas sim de:

### 🔵 Caminho 1 — Engenharia Econômica Estrutural

* **Escolaridade categorizada:** Fundamental, Médio, Superior.
* **Faixas etárias:** Jovem (18–29), Pico (30–49), Pós-pico (50+).
* **Dummy de formalidade forte:** Combinação de carteira + posição na ocupação.
* **Interações Geográficas:** UF × Escolaridade ou Região Metropolitana.

### 🟣 Caminho 2 — Tuning Sistemático

* Aplicação de **Optuna** para busca de `depth`, `learning_rate` e regularização.
* Ganho estimado: **0.01 – 0.03** no .

### 🔴 Caminho 3 — Redefinir Avaliação

* Analisar o **R² por faixa de renda** (o modelo pode performar melhor em rendas médias).
* Erro percentual médio e desempenho por UF.

---

## 7. Decisão Recomendada

**Desenvolver uma V8 focada em Engenharia Econômica Estrutural.**

**Justificativa:** O ganho marginal virá de variáveis com maior significado socioeconômico, o que torna o trabalho mais robusto para fins acadêmicos do que um simples "fine-tuning" de hiperparâmetros.

---

## 8. Conclusão Geral

O projeto percorreu o ciclo:

1. Modelo funcional
2. Modelo estável
3. Modelo otimizado
4. **Limite estrutural (Atual)**

O progresso é metodologicamente sólido. O próximo avanço exigirá uma modelagem econômica mais refinada das variáveis existentes.