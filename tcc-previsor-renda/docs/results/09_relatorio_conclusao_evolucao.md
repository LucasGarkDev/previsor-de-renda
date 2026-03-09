# RELATORIO CONSOLIDADO DE EVOLUCAO DO MODELO PREDITIVO

Projeto: Previsor de Renda com Microdados da PNAD Continua

## 1. Objetivo da Modelagem

O objetivo desta etapa do projeto foi desenvolver e avaliar modelos preditivos capazes de estimar a variavel `renda_mensal_ocupacao_principal_deflacionado`, utilizando microdados da PNAD Continua, com foco em:

- Maximizacao da capacidade preditiva (R2 e erro)
- Consistencia metodologica
- Reprodutibilidade experimental
- Comparacao entre modelagem estrutural e machine learning

Alem disso, buscou-se responder empiricamente a seguinte questao:

> Modelos de Machine Learning superam substancialmente modelos estruturais classicos na previsao de renda?

## 2. Consolidacao do Dataset

A versao final utilizada para treinamento e avaliacao foi a versao `v3` do pipeline de processamento.

Arquivo de teste:

`data/processed/v3/test.parquet`

Caracteristicas:

- 25.801 observacoes
- 24 colunas
- Target: renda mensal deflacionada
- Features socioeconomicas, demograficas e ocupacionais
- Variaveis derivadas (`idade2`, interacoes, experiencia aproximada)

Foi gerado um hash MD5 do dataset para garantir reprodutibilidade:

`9630ddbb831589d2dd50c586b7201ab5`

Todas as avaliacoes comparativas foram realizadas utilizando exatamente esse conjunto de teste.

## 3. Evolucao da Modelagem

A modelagem seguiu uma trajetoria incremental e metodologicamente controlada.

### 3.1 Fase 1 - Modelos Lineares Regularizados

Foi inicialmente implementado um modelo ElasticNet como baseline.

Objetivo:

- Estabelecer referencia econometrica regularizada

Resultado aproximado:

- R2 log ~= 0.44

Conclusao:
Modelos lineares simples capturam parte relevante da variancia, porem apresentam limitacao na modelagem de nao linearidades e interacoes complexas.

### 3.2 Fase 2 - Gradient Boosting

Foram testados modelos baseados em arvores:

- HistGradientBoosting
- XGBoost

Esses modelos apresentaram melhora significativa em relacao ao baseline linear, capturando relacoes nao lineares entre escolaridade, idade, ocupacao e renda.

### 3.3 Fase 3 - CatBoost

Foi adotado o CatBoost devido a:

- Tratamento nativo de variaveis categoricas
- Reducao da necessidade de encoding manual
- Robustez para dados tabulares heterogeneos

A melhor versao consolidada foi:

`CatBoost V5 Global`

Metricas no conjunto de teste (`v3`):

Espaco logaritmico:

- R2 log: 0.5913
- RMSE log: 0.5721
- MAE log: 0.4330

Escala original:

- R2: 0.4635
- RMSE: 934.09
- MAE: 482.82

Esse modelo representou o melhor desempenho puramente algoritmico.

## 4. Implementacao do Modelo Hibrido (Mincer + CatBoost)

Foi entao proposta uma abordagem hibrida com o objetivo de integrar:

- Estrutura economica classica
- Aprendizado nao linear residual

### 4.1 Estrutura do Modelo Hibrido

Etapas:

1. Modelo estrutural baseado na equacao de Mincer com:
   - `anos_estudo`
   - `experiencia_aprox`
   - `idade2`
   - `sexo`
   - `regiao`
   - `carteira assinada`
2. Transformacao da renda para log.
3. Calculo dos residuos estruturais.
4. Treinamento do CatBoost sobre os residuos.
5. Recombinacao final:

```text
log(y^) = y^Mincer + residuo^
y^ = exp(log(y^)) x smearing
```

Essa abordagem separa o componente estrutural (interpretavel) do componente nao linear (algoritmico).

### 4.2 Resultados do Hybrid V1

Metricas no mesmo conjunto de teste (`v3`):

Espaco log:

- R2 log: 0.5889
- RMSE log: 0.5738
- MAE log: 0.4345

Escala original:

- R2: 0.4906
- RMSE: 910.17
- MAE: 528.32

## 5. Comparacao Justa entre Modelos

Comparacao consolidada:

| Modelo | R2 log | R2 original |
| --- | ---: | ---: |
| CatBoost V5 | 0.5913 | 0.4635 |
| Hybrid V1 | 0.5889 | 0.4906 |

## 6. Interpretacao dos Resultados

### 6.1 No espaco de aprendizado (log)

O CatBoost puro apresentou desempenho marginalmente superior:

`0.5913 vs 0.5889`

A diferenca e pequena.

### 6.2 Na escala original

O modelo hibrido apresentou:

- R2 maior
- RMSE menor
- MAE ligeiramente maior

Isso sugere que o hibrido reduz melhor erros quadraticos (impacto de grandes desvios), embora aumente ligeiramente o erro absoluto medio.

## 7. Conclusao Cientifica

- A maior parte da variancia da renda e explicada por variaveis estruturais classicas (educacao, experiencia, ocupacao).
- O ganho adicional proporcionado pelo Machine Learning puro e pequeno.
- A abordagem hibrida mantem desempenho competitivo.
- A diferenca entre modelos e marginal.

Esses resultados estao alinhados com a literatura contemporanea que argumenta que modelos de Machine Learning frequentemente melhoram previsoes, mas nao substituem completamente a estrutura economica bem especificada.

## 8. Contribuicao Metodologica

A principal contribuicao do projeto foi:

- Implementacao de pipeline reprodutivel
- Comparacao empirica justa
- Integracao entre econometria estrutural e aprendizado de maquina
- Analise critica dos limites preditivos da base

O modelo hibrido oferece:

- Interpretabilidade estrutural
- Robustez algoritmica
- Coerencia teorica
- Competitividade preditiva

## 9. Limitacoes

- Ausencia de variaveis nao observaveis (ex.: qualidade da escola, background familiar)
- Dados transversais (nao longitudinais)
- Limitacao informacional intrinseca a base
- Retornos decrescentes observados nas tentativas de melhoria incremental

## 10. Estado Atual do Projeto

O modelo encontra-se em estagio maduro:

- Dataset consolidado
- Avaliacao padronizada
- Smearing corretamente aplicado
- Comparacao reprodutivel
- Resultados estaveis

Do ponto de vista tecnico e cientifico, o modelo atingiu um nivel adequado para encerramento da etapa de modelagem.
