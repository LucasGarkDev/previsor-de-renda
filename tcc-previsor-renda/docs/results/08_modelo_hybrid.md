# 📄 RELATÓRIO DE EVOLUÇÃO DO MODELO

**Projeto:** Previsor de Renda — PNAD Contínua

**Versão:** Consolidada até Hybrid V1

---

## 1️⃣ Objetivo do Projeto

Desenvolver um modelo preditivo capaz de estimar a renda mensal do trabalho principal (deflacionada), combinando engenharia de features socioeconômicas, modelos econométricos estruturais e algoritmos de Machine Learning.

**Objetivo Secundário:** Avaliar empiricamente se modelos puramente algorítmicos superam uma modelagem estrutural baseada na **Equação de Mincer**.

---

## 2️⃣ Consolidação do Dataset

* **Versão:** v3
* **Arquivo:** `data/processed/v3/test.parquet`
* **Assinatura (Hash MD5):** `9630ddbb831589d2dd50c586b7201ab5`

**Estrutura dos Dados:**

* **Amostra:** 25.801 observações (set de teste).
* **Target:** `renda_mensal_ocupacao_principal_deflacionado`.
* **Features:** Escolaridade, Experiência aproximada, Idade (e interações), Características ocupacionais, Região, Indicadores urbanos e Carteira assinada.

---

## 3️⃣ Linha do Tempo da Modelagem

### 🔹 Fase 1 — Modelos Lineares (ElasticNet)

* **Objetivo:** Estabelecer baseline econométrico regularizado.
* **Resultado:** $R^2$ log $\approx 0.44$.
* **Conclusão:** Insuficiente para capturar não-linearidades complexas.

### 🔹 Fase 2 & 3 — Boosting Inicial (HistGradient & XGBoost)

* Melhora moderada, porém exigiu *tuning* manual intenso para lidar com a natureza dos dados.

### 🔹 Fase 4 — CatBoost (Modelos v4, v5, v6)

* **Motivação:** Tratamento nativo de variáveis categóricas e robustez tabular.
* **📌 Performance CatBoost V5 Global:**

| Métrica | Escala LOG | Escala Original |
| --- | --- | --- |
| **$R^2$** | **0.5913** | 0.4635 |
| **RMSE** | 0.5721 | 934.09 |
| **MAE** | 0.4330 | 482.82 |

---

## 4️⃣ Fase 5 — Modelo Híbrido (Mincer + ML)

**Estrutura do Hybrid V1:**

1. **Componente Estrutural:** Regressão Linear baseada em Mincer (anos de estudo, experiência, idade², sexo, região, carteira).
2. **Componente Residual:** CatBoost treinado exclusivamente sobre os resíduos do modelo linear.
3. **Recombinação:**

$$log\_pred = mincer\_pred + residual\_pred$$


$$renda\_pred = \exp(log\_pred) \cdot smearing$$



**📌 Resultado Oficial Hybrid V1:**

* **$R^2$ Log:** 0.5889
* **$R^2$ Original:** **0.4906**
* **RMSE Original:** **910.17**

---

## 5️⃣ Comparação Final Justa

| Modelo | $R^2$ log | $R^2$ original |
| --- | --- | --- |
| **CatBoost V5** | **0.5913** | 0.4635 |
| **Hybrid V1** | 0.5889 | **0.4906** |

---

## 6️⃣ Interpretação Técnica

* **No espaço log (aprendizado):** O CatBoost puro é marginalmente superior ($0.5913$ vs $0.5889$), mas a diferença é desprezível.
* **Na escala original (valor real):** O modelo **Híbrido** apresenta $R^2$ maior e RMSE menor, sugerindo um melhor ajuste global e redução do erro quadrático médio.

---

## 7️⃣ Conclusão Científica

1. A maior parte da variância da renda é explicada por variáveis estruturais clássicas.
2. O ganho do Machine Learning "puro" sobre a estrutura econômica é pequeno.
3. O **modelo híbrido** mantém a interpretabilidade econômica sem perda significativa de performance, sendo mais defensável academicamente.

---

## 8️⃣ Próximos Passos Sugeridos

* [ ] Rodar validação cruzada temporal.
* [ ] Analisar a importância das features (Feature Importance) no CatBoost residual.
* [ ] Decompor formalmente a variância explicada por cada componente (estrutural vs. não-linear).
* [ ] Redigir a seção de "Discussão e Implicações" para o artigo/relatório final.

---

### 🎯 Pergunta Final do Projeto

**O Machine Learning supera a modelagem estrutural tradicional?**
*Resposta empírica:* Supera **marginalmente** no espaço log, mas não de forma substancial na escala original. O modelo híbrido é a escolha ótima por equilibrar competitividade e interpretabilidade.