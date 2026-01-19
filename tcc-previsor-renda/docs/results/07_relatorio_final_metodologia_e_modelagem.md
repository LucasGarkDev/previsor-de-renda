# Relatório Final de Metodologia e Modelagem  
**Projeto:** Previsor de Renda Individual  
**Base de Dados:** PNAD Contínua – IBGE (Base dos Dados / BigQuery)  
**Autor:** [Seu nome]  
**Curso:** [Seu curso]  
**Instituição:** [Sua instituição]  
**Ano:** 2026  

---

## 1. Introdução

Este relatório consolida **todas as etapas metodológicas e experimentais realizadas até o momento** no desenvolvimento do Trabalho de Conclusão de Curso cujo objetivo é a **predição da renda mensal do trabalho principal de indivíduos brasileiros**, a partir de dados da PNAD Contínua.

O trabalho foi estruturado de forma incremental, com foco em:

- Reprodutibilidade;
- Clareza metodológica;
- Comparação controlada entre modelos;
- Coerência estatística e econômica;
- Análise crítica de riscos como *overfitting* e *proxy leakage*.

---

## 2. Visão Geral do Pipeline de Dados

O projeto foi estruturado como um **pipeline modular**, dividido em etapas bem definidas:

1. Extração dos dados (BigQuery);
2. Limpeza e transformação;
3. Engenharia de atributos;
4. Divisão treino / validação / teste;
5. Treinamento de modelos;
6. Avaliação final em conjunto de teste.

Cada etapa é versionada, rastreável e executável de forma independente.

---

## 3. Pipeline V1 — Modelagem Baseline

### 3.1 Fonte dos Dados

- PNAD Contínua – nível **pessoa**
- Extração via BigQuery (Base dos Dados)

### 3.2 Modelos Avaliados (V1)

Foram avaliados quatro modelos:

- ElasticNet (baseline linear);
- HistGradientBoostingRegressor;
- XGBoost Regressor;
- CatBoost Regressor.

Todos foram treinados e avaliados com o mesmo conjunto de teste.

### 3.3 Resultados Comparativos (V1)

| Modelo | RMSE | MAE | R² |
|------|------|------|----|
| ElasticNet | 2.471,84 | 1.573,68 | 0,1802 |
| HistGradientBoosting | 2.420,11 | 1.503,42 | 0,2140 |
| XGBoost | 2.512,33 | 1.545,02 | 0,1541 |
| **CatBoost** | **2.386,92** | **1.471,60** | **0,2356** |

### 3.4 Conclusão do Pipeline V1

- Modelos não lineares superaram o baseline linear;
- O CatBoost apresentou o melhor equilíbrio entre desempenho e estabilidade;
- R² moderado era esperado para um problema socioeconômico individual.

---

## 4. Pipeline V2 — Enriquecimento Contextual

### 4.1 Motivação

A renda individual é fortemente influenciada pelo **contexto domiciliar**. Assim, foi criada uma segunda versão do pipeline para incorporar essas informações de forma explícita.

### 4.2 Integração de Dados

Foram utilizadas duas tabelas:

- `microdados_pessoa`
- `microdados_compatibilizados_domicilio`

A integração foi realizada via:

```text
LEFT JOIN por id_domicilio
```

Essa estratégia garante que todos os indivíduos da tabela de pessoas sejam mantidos no conjunto final, mesmo que eventualmente não haja correspondência completa no cadastro domiciliar.

O resultado é um dataset enriquecido, que combina atributos individuais e contextuais, ampliando o espaço de informação disponível para os modelos.

---

## 10. Encaminhamento para a Etapa de Software

Com o modelo final definido, o próximo passo do projeto consiste em sua materialização como um sistema funcional. As principais ações previstas são:

- Criar uma **API backend em Python**, preferencialmente utilizando o framework **FastAPI**;
- Carregar o modelo treinado por meio de `joblib`;
- Receber dados de entrada via requisições HTTP (formulário ou JSON);
- Retornar a renda prevista como resposta da API;
- Desenvolver um **frontend em React** para interação com o usuário, contendo:
  - Formulário de entrada de dados;
  - Validação básica dos campos;
  - Exibição clara do valor de renda previsto.

Essa etapa não altera os resultados estatísticos, mas transforma o modelo em um produto computacional utilizável, alinhado à proposta prática do TCC.

---

## 11. Conclusão

O projeto apresenta:

- Um pipeline sólido, modular e versionado;
- Metodologia clara e reprodutível;
- Comparações justas entre diferentes classes de modelos;
- Análise crítica e responsável dos resultados;
- Consistência estatística e fundamentação econômica;
- Base técnica robusta para evolução em software aplicado.

A pesquisa encontra-se, portanto, pronta para a transição da **fase analítica e experimental** para a **fase de implementação do sistema**, consolidando o trabalho como um projeto completo de ciência de dados aplicada.
