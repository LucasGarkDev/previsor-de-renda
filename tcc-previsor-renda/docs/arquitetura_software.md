# Arquitetura de Software  
**Projeto:** Previsor de Renda  
**Tecnologias:** Python, Machine Learning, React  
**Contexto:** Trabalho de Conclusão de Curso  

---

## 1. Visão Geral da Arquitetura

O sistema desenvolvido neste projeto adota uma **arquitetura modular em camadas**, separando claramente:

- processamento e modelagem de dados;
- lógica de inferência do modelo treinado;
- interface de interação com o usuário final.

Essa separação permite:
- reprodutibilidade científica;
- manutenção independente dos componentes;
- clareza metodológica e arquitetural para fins acadêmicos.

A arquitetura completa é composta por **três grandes blocos**:

1. Pipeline de Machine Learning (offline);
2. Backend de inferência (online);
3. Frontend de interação com o usuário.

---

## 2. Pipeline de Machine Learning (Camada Analítica)

### 2.1 Papel do Pipeline

O pipeline de Machine Learning é responsável por todo o **ciclo analítico offline**, incluindo:

- extração de dados da PNAD Contínua;
- limpeza e transformação;
- engenharia de atributos;
- treinamento de modelos;
- avaliação e comparação;
- análise de interpretabilidade;
- exportação do modelo final.

Esse pipeline **não é executado em tempo real** e não faz parte do fluxo de uso do sistema pelo usuário final.

---

### 2.2 Organização do Pipeline

O pipeline foi implementado como um módulo independente (`ml_pipeline`), estruturado de forma modular:

- `data/`: ingestão, transformação e divisão dos dados;
- `models/`: treinamento, avaliação, SHAP e exportação;
- `pipelines/`: orquestração das etapas;
- `config/`: parâmetros globais e caminhos;
- `utils/`: logging, leitura e persistência.

Essa organização permite:
- substituição de modelos sem alterar o fluxo;
- comparação formal entre algoritmos;
- rastreabilidade completa dos experimentos.

---

### 2.3 Saída do Pipeline

O pipeline gera como artefatos finais:

- modelo treinado serializado (`.joblib`);
- métricas de avaliação;
- resultados de interpretabilidade;
- documentação dos experimentos.

Esses artefatos são versionados e posteriormente **consumidos pelo backend de inferência**.

---

## 3. Backend de Inferência (Camada de Serviço)

### 3.1 Papel do Backend

O backend em Python tem como responsabilidade **exclusiva** disponibilizar o modelo treinado para uso externo, por meio de um **único caso de uso**:

> Dado um conjunto de características individuais informadas por um usuário, estimar a renda mensal do trabalho principal.

O backend **não realiza treinamento**, apenas:
- carrega o modelo final;
- valida os dados de entrada;
- executa a inferência;
- retorna a previsão.

---

### 3.2 Natureza do Caso de Uso

O sistema foi propositalmente projetado com **apenas um caso de uso**, garantindo:

- simplicidade arquitetural;
- clareza de escopo;
- alinhamento com o objetivo do TCC.

Fluxo lógico do backend:

1. Receber dados do frontend via API;
2. Validar estrutura e tipos;
3. Adaptar os dados ao formato esperado pelo modelo;
4. Executar a predição;
5. Retornar o valor estimado de renda.

---

### 3.3 Independência do Modelo

O backend é desacoplado do pipeline de treinamento.  
A troca do modelo (por exemplo, ElasticNet → CatBoost) **não exige alterações no backend**, desde que o contrato de entrada seja mantido.

Essa decisão arquitetural garante:
- flexibilidade futura;
- separação clara entre ciência de dados e engenharia de software.

---

## 4. Frontend (Camada de Apresentação)

### 4.1 Papel do Frontend

O frontend, implementado em **React**, é responsável por:

- coletar informações do usuário por meio de um formulário;
- validar dados no nível de interface;
- enviar as informações ao backend;
- exibir a renda prevista de forma clara.

O frontend **não contém lógica estatística ou de ML**.

---

### 4.2 Natureza da Interação

A interação com o usuário é:

- direta;
- determinística;
- focada em simulação individual.

O sistema não realiza armazenamento de dados pessoais nem aprendizado contínuo.

---

## 5. Fluxo Completo do Sistema

O fluxo de funcionamento do sistema pode ser resumido da seguinte forma:

1. O pipeline de ML é executado offline;
2. O modelo final é treinado, avaliado e exportado;
3. O backend carrega o modelo exportado;
4. O usuário preenche um formulário no frontend;
5. O frontend envia os dados ao backend;
6. O backend executa a inferência;
7. A renda estimada é retornada ao usuário.

---

## 6. Decisões Arquiteturais Fundamentais

As principais decisões arquiteturais adotadas foram:

- separação total entre treino e inferência;
- pipeline independente e reprodutível;
- backend minimalista com um único caso de uso;
- frontend desacoplado da lógica de ML;
- foco em clareza e robustez, não em escalabilidade extrema.

Essas decisões são coerentes com o caráter acadêmico do projeto.

---

## 7. Escopo e Limitações

Este projeto **não tem como objetivo**:

- aprendizado online;
- múltiplos modelos concorrentes em produção;
- armazenamento histórico de previsões;
- autenticação ou personalização de usuários.

Essas funcionalidades são consideradas extensões futuras possíveis, mas fora do escopo do TCC.

---

## 8. Considerações Finais

A arquitetura proposta atende plenamente aos objetivos do trabalho, equilibrando:

- rigor científico;
- boas práticas de engenharia de software;
- simplicidade conceitual;
- clareza para avaliação acadêmica.

O sistema foi projetado para demonstrar, de forma transparente, como um modelo de Machine Learning pode ser integrado a uma aplicação real, mantendo separação de responsabilidades e interpretabilidade.

---
