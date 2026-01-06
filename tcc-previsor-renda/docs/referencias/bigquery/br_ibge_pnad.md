# Dataset `br_ibge_pnad`

## Tabela `dicionario`

**Descrição:** Dicionário para tradução dos códigos do conjunto br_ibge_pnad. Para taduzir códigos compartilhados entre instituições, como id_municipio, buscar por diretórios

- Linhas aproximadas: 142
- Tamanho aproximado (MB): 0.01

### Esquema de colunas

| Coluna | Tipo | Modo | Descrição |
|--------|------|------|-----------|
| id_tabela | STRING | NULLABLE | ID Tabela |
| nome_coluna | STRING | NULLABLE | Nome da coluna |
| chave | STRING | NULLABLE | Chave |
| cobertura_temporal | STRING | NULLABLE | Cobertura Temporal |
| valor | STRING | NULLABLE | Valor |

### Exemplo de dados (5 linhas)

| id_tabela                             | nome_coluna     |   chave | cobertura_temporal   | valor         |
|:--------------------------------------|:----------------|--------:|:---------------------|:--------------|
| microdados_compatibilizados_pessoa    | grupos_ocupacao |         | (1)                  | não aplicável |
| microdados_compatibilizados_pessoa    | sexo            |       0 | (1)                  | mulher        |
| microdados_compatibilizados_domicilio | possui_tv       |       0 | (1)                  | não           |
| microdados_compatibilizados_domicilio | zona_urbana     |       0 | (1)                  | rural         |
| microdados_compatibilizados_domicilio | possui_fogao    |       0 | (1)                  | não           |

---

## Tabela `microdados_compatibilizados_domicilio`

**Descrição:** Microdados da PNAD a nível de domicílio

- Linhas aproximadas: 1877416
- Tamanho aproximado (MB): 305.35

### Esquema de colunas

| Coluna | Tipo | Modo | Descrição |
|--------|------|------|-----------|
| ano | INTEGER | NULLABLE | Ano da pesquisa |
| id_regiao | STRING | NULLABLE | ID da Região - IBGE |
| id_uf | STRING | NULLABLE | ID Unidade da Federação - IBGE |
| sigla_uf | STRING | NULLABLE | Sigla da Unidade da Federação |
| id_domicilio | STRING | NULLABLE | Número de identificação do domicílio |
| regiao_metropolitana | INTEGER | NULLABLE | Região Metropolitana (0 = Não e 1 = Sim) |
| zona_urbana | STRING | NULLABLE | Zona Urbana |
| tipo_zona_domicilio | STRING | NULLABLE | Tipo de zona do domicílio |
| total_pessoas | INTEGER | NULLABLE | Total de pessoas |
| total_pessoas_10_mais | INTEGER | NULLABLE | Total de pessoas 10 anos ou mais |
| especie_domicilio | STRING | NULLABLE | Espécie de domicílio |
| tipo_domicilio | STRING | NULLABLE | Tipo de domicílio |
| tipo_parede | STRING | NULLABLE | Material Predominante das paredes |
| tipo_cobertura | STRING | NULLABLE | Material Predominante no telhado |
| possui_agua_rede | STRING | NULLABLE | Água provém de rede? |
| tipo_esgoto | STRING | NULLABLE | Esgotamento sanitário |
| possui_sanitario_exclusivo | STRING | NULLABLE | Sanitário exclusivo do domicílio? |
| lixo_coletado | STRING | NULLABLE | O lixo é coletado? |
| possui_iluminacao_eletrica | STRING | NULLABLE | Possui iluminação elétrica? |
| quantidade_comodos | INTEGER | NULLABLE | Quantidade de cômodos |
| quantidade_dormitorios | INTEGER | NULLABLE | Quantidade de cômodos servindo como dormitório |
| possui_sanitario | STRING | NULLABLE | Possui sanitário? |
| posse_domicilio | STRING | NULLABLE | Posse do domicílio |
| possui_filtro | STRING | NULLABLE | Possui filtro? |
| possui_fogao | STRING | NULLABLE | Possui fogão? |
| possui_geladeira | STRING | NULLABLE | Possui geladeira? |
| possui_radio | STRING | NULLABLE | Possui rádio? |
| possui_tv | STRING | NULLABLE | Possui televisão? |
| renda_mensal_domiciliar | FLOAT | NULLABLE | Renda mensal domiciliar |
| renda_mensal_domiciliar_compativel_1992 | FLOAT | NULLABLE | Renda mensal domiciliar compatível com 1992 |
| aluguel | FLOAT | NULLABLE | Valor do aluguel |
| prestacao | FLOAT | NULLABLE | Valor da prestação |
| deflator | INTEGER | NULLABLE | Deflator (base outubro de 2012) |
| conversor_moeda | INTEGER | NULLABLE | Conversor de Moeda |
| renda_domicilio_deflacionado | FLOAT | NULLABLE | Renda do domicílio - Valor deflacionado |
| renda_mensal_domiciliar_compativel_1992_deflacionado | FLOAT | NULLABLE | Renda mensal domiciliar compatível com 1992 - Valor deflacionado |
| aluguel_deflacionado | FLOAT | NULLABLE | Aluguel - Valor deflacionado |
| prestacao_deflacionado | FLOAT | NULLABLE | Prestação - Valor deflacionado |
| peso_amostral | FLOAT | NULLABLE | Peso do domicílio |

### Exemplo de dados (5 linhas)

|   ano |   id_regiao |   id_uf | sigla_uf   |   id_domicilio |   regiao_metropolitana |   zona_urbana |   tipo_zona_domicilio |   total_pessoas |   total_pessoas_10_mais |   especie_domicilio | tipo_domicilio   | tipo_parede   | tipo_cobertura   | possui_agua_rede   | tipo_esgoto   | possui_sanitario_exclusivo   | lixo_coletado   | possui_iluminacao_eletrica   | quantidade_comodos   | quantidade_dormitorios   | possui_sanitario   | posse_domicilio   | possui_filtro   | possui_fogao   | possui_geladeira   | possui_radio   | possui_tv   |   renda_mensal_domiciliar |   renda_mensal_domiciliar_compativel_1992 |   aluguel |   prestacao |   deflator |   conversor_moeda |   renda_domicilio_deflacionado |   renda_mensal_domiciliar_compativel_1992_deflacionado |   aluguel_deflacionado |   prestacao_deflacionado |   peso_amostral |
|------:|------------:|--------:|:-----------|---------------:|-----------------------:|--------------:|----------------------:|----------------:|------------------------:|--------------------:|:-----------------|:--------------|:-----------------|:-------------------|:--------------|:-----------------------------|:----------------|:-----------------------------|:---------------------|:-------------------------|:-------------------|:------------------|:----------------|:---------------|:-------------------|:---------------|:------------|--------------------------:|------------------------------------------:|----------:|------------:|-----------:|------------------:|-------------------------------:|-------------------------------------------------------:|-----------------------:|-------------------------:|----------------:|
|  1998 |           1 |      16 | AP         |  9816000064004 |                      0 |             1 |                     2 |               2 |                       2 |                   5 |                  |               |                  |                    |               |                              |                 |                              | <NA>                 | <NA>                     |                    |                   |                 |                |                    |                |             |                       nan |                                        65 |       nan |         nan |          0 |                 1 |                            nan |                                                    163 |                    nan |                      nan |             322 |
|  1998 |           1 |      13 | AM         |  9813000497002 |                      0 |             1 |                     2 |               9 |                       7 |                   5 |                  |               |                  |                    |               |                              |                 |                              | <NA>                 | <NA>                     |                    |                   |                 |                |                    |                |             |                       nan |                                       250 |       nan |         nan |          0 |                 1 |                            nan |                                                    626 |                    nan |                      nan |             401 |
|  1998 |           1 |      13 | AM         |  9813000497009 |                      0 |             1 |                     2 |               5 |                       3 |                   3 |                  |               |                  |                    |               |                              |                 |                              | <NA>                 | <NA>                     |                    |                   |                 |                |                    |                |             |                       nan |                                       350 |       nan |         nan |          0 |                 1 |                            nan |                                                    876 |                    nan |                      nan |             401 |
|  1998 |           1 |      13 | AM         |  9813000551010 |                      0 |             1 |                     2 |              10 |                       9 |                   5 |                  |               |                  |                    |               |                              |                 |                              | <NA>                 | <NA>                     |                    |                   |                 |                |                    |                |             |                       nan |                                       760 |       nan |         nan |          0 |                 1 |                            nan |                                                   1902 |                    nan |                      nan |             401 |
|  1998 |           1 |      13 | AM         |  9813000640004 |                      0 |             1 |                     2 |               4 |                       4 |                   3 |                  |               |                  |                    |               |                              |                 |                              | <NA>                 | <NA>                     |                    |                   |                 |                |                    |                |             |                       nan |                                       250 |       nan |         nan |          0 |                 1 |                            nan |                                                    626 |                    nan |                      nan |             401 |

---

## Tabela `microdados_compatibilizados_pessoa`

**Descrição:** Microdados da PNAD a nível de pessoa

- Linhas aproximadas: 7710243
- Tamanho aproximado (MB): 1240.67

### Esquema de colunas

| Coluna | Tipo | Modo | Descrição |
|--------|------|------|-----------|
| ano | INTEGER | NULLABLE | Ano da pesquisa |
| id_regiao | STRING | NULLABLE | ID da Região - IBGE |
| id_uf | STRING | NULLABLE | ID Unidade da Federação - IBGE |
| sigla_uf | STRING | NULLABLE | Sigla da Unidade da Federação |
| id_domicilio | STRING | NULLABLE | Número de identificação do domicílio |
| regiao_metropolitana | STRING | NULLABLE | Região Metropolitana (0 = Não e 1 = Sim) |
| numero_familia | INTEGER | NULLABLE | Número da família |
| ordem | INTEGER | NULLABLE | Número de ordem da pessoa |
| condicao_domicilio | STRING | NULLABLE | Condição no domicílio |
| condicao_familia | STRING | NULLABLE | Condição na família |
| numero_membros_familia | INTEGER | NULLABLE | Número de membros da família |
| sexo | STRING | NULLABLE | Sexo |
| dia_nascimento | INTEGER | NULLABLE | Dia de nascimento |
| mes_nascimento | INTEGER | NULLABLE | Mês de nascimento |
| ano_nascimento | INTEGER | NULLABLE | Ano do nascimento |
| idade | INTEGER | NULLABLE | Idade |
| raca_cor | STRING | NULLABLE | Raça ou Cor (autodeclaração) |
| sabe_ler_escrever | STRING | NULLABLE | Sabe ler e escrever |
| frequenta_escola | STRING | NULLABLE | Frequenta a escola |
| serie_frequentada | STRING | NULLABLE | Série que frequenta |
| grau_frequentado | STRING | NULLABLE | Grau que frequenta |
| ultima_serie_frequentada | INTEGER | NULLABLE | Última série frequentada (para quem não frequenta escola) |
| ultimo_grau_frequentado | STRING | NULLABLE | Último grau frequentado (para quem não frequenta escola) |
| anos_estudo | INTEGER | NULLABLE | Anos de estudo |
| trabalhou_semana | STRING | NULLABLE | Trabalhou na semana |
| tinha_trabalhado_semana | STRING | NULLABLE | Tinha trabalhado na semana |
| tinha_outro_trabalho | STRING | NULLABLE | Tinha outro trabalho na semana de referência |
| ocupacao_semana | INTEGER | NULLABLE | Ocupação na semana |
| atividade_ramo_negocio_semana | INTEGER | NULLABLE | Atividade ou ramo do négocio na semana |
| atividade_ramo_negocio_anterior | STRING | NULLABLE | Atividade ou ramo do negócio anterior |
| possui_carteira_assinada | STRING | NULLABLE | Tem carteira de trabalho assinada |
| renda_mensal_dinheiro | FLOAT | NULLABLE | Rendimento mensal em dinheiro |
| renda_mensal_produto_mercadoria | FLOAT | NULLABLE | Rendimento mensal em produtos ou mercadorias |
| horas_trabalhadas_semana | INTEGER | NULLABLE | Horas normalmente trabalhadas na semana - Ocupação principal |
| renda_mensal_dinheiro_outra | FLOAT | NULLABLE | Rendimento mensal em dinheiro ou outras fontes |
| renda_mensal_produto_outra | FLOAT | NULLABLE | Rendimento mensal em produtos ou outras fontes |
| horas_trabalhadas_outros_trabalhos | INTEGER | NULLABLE | Horas normalmente trabalhadas na semana - Outros trabalhos |
| contribui_previdencia | STRING | NULLABLE | Contribui para instituto de previdência |
| tipo_instituto_previdencia | STRING | NULLABLE | Tipo de instituto de previdência |
| tomou_providencia_conseguir_trabalho_semana | STRING | NULLABLE | Tomou providência para conseguir trabalho na semana |
| tomou_providencia_ultimos_2_meses | STRING | NULLABLE | Tomou providência nos últimos 2 meses para conseguir trabalho |
| qual_providencia_tomou | STRING | NULLABLE | O que foi tomado de medida para encontrar um emprego |
| tinha_carteira_assinada_ultimo_emprego | STRING | NULLABLE | Tinha carteira assinada no último emprego |
| renda_aposentadoria | FLOAT | NULLABLE | Valor da Aposentadoria |
| renda_pensao | FLOAT | NULLABLE | Valor da Pensão |
| renda_abono_permanente | FLOAT | NULLABLE | Valor do bônus do salário permanente |
| renda_aluguel | FLOAT | NULLABLE | Valor do Aluguel recebido |
| renda_outras | FLOAT | NULLABLE | Valor de outras rendas |
| renda_mensal_ocupacao_principal | FLOAT | NULLABLE | Rendimento mensal ocupação principal |
| renda_mensal_todos_trabalhos | FLOAT | NULLABLE | Rendimento mensal todos trabalhos |
| renda_mensal_todas_fontes | FLOAT | NULLABLE | Rendimento mensal todas fontes |
| atividade_ramo_negocio_agregado | STRING | NULLABLE | Atividade ou ramo do négocio na semana - Agregado |
| horas_trabalhadas_todos_trabalhos | INTEGER | NULLABLE | Horas normalmente trabalhadas na semana em todos os trabalhos |
| posicao_ocupacao | STRING | NULLABLE | Posição de ocupação na semana |
| grupos_ocupacao | STRING | NULLABLE | Grupos de ocupação na semana |
| renda_mensal_familia | FLOAT | NULLABLE | Rendimento mensal da família |
| ocupacao_ano_anterior | STRING | NULLABLE | Ocupação no ano anterior |
| renda_mensal_dinheiro_deflacionado | FLOAT | NULLABLE | Rendimento mensal em dinheiro - Valor deflacionado |
| renda_mensal_produto_mercadoria_deflacionado | FLOAT | NULLABLE | Rendimento mensal em produto ou mercadoria - Valor deflacionado |
| renda_mensal_dinheiro_outra_deflacionado | FLOAT | NULLABLE | Rendimento mensal em dinheiro outra - Valor deflacionado |
| renda_mensal_produto_mercadoria_outra_deflacionado | FLOAT | NULLABLE | Rendimento mensal em produto ou mercadoria outra - Valor deflacionado |
| renda_mensal_ocupacao_principal_deflacionado | FLOAT | NULLABLE | Rendimento mensal da ocupação principal - Valor deflacionado |
| renda_mensal_todos_trabalhos_deflacionado | FLOAT | NULLABLE | Rendimento mensal de todos os trabalhos - Valor deflacionado |
| renda_mensal_todas_fontes_deflacionado | FLOAT | NULLABLE | Rendimento mensal de todas as fontes - Valor deflacionado |
| renda_mensal_familia_deflacionado | FLOAT | NULLABLE | Rendimento mensal da família - Valor deflacionado |
| renda_aposentadoria_deflacionado | FLOAT | NULLABLE | Valor da aposentadoria - Valor deflacionado |
| renda_pensao_deflacionado | FLOAT | NULLABLE | Valor da Pensão - Valor deflacionado |
| renda_abono_deflacionado | FLOAT | NULLABLE | Valor do abono - Valor deflacionado |
| renda_aluguel_deflacionado | FLOAT | NULLABLE | Valor do Aluguel - Valor deflacionado |
| renda_outras_deflacionado | FLOAT | NULLABLE | Rendas Outras - Valor deflacionado |

### Exemplo de dados (5 linhas)

|   ano |   id_regiao |   id_uf | sigla_uf   |    id_domicilio |   regiao_metropolitana |   numero_familia |   ordem |   condicao_domicilio |   condicao_familia | numero_membros_familia   |   sexo |   dia_nascimento |   mes_nascimento |   ano_nascimento |   idade |   raca_cor |   sabe_ler_escrever |   frequenta_escola |   serie_frequentada |   grau_frequentado | ultima_serie_frequentada   | ultimo_grau_frequentado   |   anos_estudo | trabalhou_semana   | tinha_trabalhado_semana   | tinha_outro_trabalho   | ocupacao_semana   | atividade_ramo_negocio_semana   | atividade_ramo_negocio_anterior   | possui_carteira_assinada   |   renda_mensal_dinheiro |   renda_mensal_produto_mercadoria | horas_trabalhadas_semana   |   renda_mensal_dinheiro_outra |   renda_mensal_produto_outra | horas_trabalhadas_outros_trabalhos   | contribui_previdencia   | tipo_instituto_previdencia   | tomou_providencia_conseguir_trabalho_semana   | tomou_providencia_ultimos_2_meses   | qual_providencia_tomou   | tinha_carteira_assinada_ultimo_emprego   |   renda_aposentadoria |   renda_pensao |   renda_abono_permanente |   renda_aluguel |   renda_outras |   renda_mensal_ocupacao_principal |   renda_mensal_todos_trabalhos |   renda_mensal_todas_fontes | atividade_ramo_negocio_agregado   | horas_trabalhadas_todos_trabalhos   | posicao_ocupacao   | grupos_ocupacao   |   renda_mensal_familia | ocupacao_ano_anterior   |   renda_mensal_dinheiro_deflacionado |   renda_mensal_produto_mercadoria_deflacionado |   renda_mensal_dinheiro_outra_deflacionado |   renda_mensal_produto_mercadoria_outra_deflacionado |   renda_mensal_ocupacao_principal_deflacionado |   renda_mensal_todos_trabalhos_deflacionado |   renda_mensal_todas_fontes_deflacionado |   renda_mensal_familia_deflacionado |   renda_aposentadoria_deflacionado |   renda_pensao_deflacionado |   renda_abono_deflacionado |   renda_aluguel_deflacionado |   renda_outras_deflacionado |
|------:|------------:|--------:|:-----------|----------------:|-----------------------:|-----------------:|--------:|---------------------:|-------------------:|:-------------------------|-------:|-----------------:|-----------------:|-----------------:|--------:|-----------:|--------------------:|-------------------:|--------------------:|-------------------:|:---------------------------|:--------------------------|--------------:|:-------------------|:--------------------------|:-----------------------|:------------------|:--------------------------------|:----------------------------------|:---------------------------|------------------------:|----------------------------------:|:---------------------------|------------------------------:|-----------------------------:|:-------------------------------------|:------------------------|:-----------------------------|:----------------------------------------------|:------------------------------------|:-------------------------|:-----------------------------------------|----------------------:|---------------:|-------------------------:|----------------:|---------------:|----------------------------------:|-------------------------------:|----------------------------:|:----------------------------------|:------------------------------------|:-------------------|:------------------|-----------------------:|:------------------------|-------------------------------------:|-----------------------------------------------:|-------------------------------------------:|-----------------------------------------------------:|-----------------------------------------------:|--------------------------------------------:|-----------------------------------------:|------------------------------------:|-----------------------------------:|----------------------------:|---------------------------:|-----------------------------:|----------------------------:|
|  2005 |           1 |      16 | AP         | 200516000013008 |                      0 |                1 |       4 |                    3 |                  3 | <NA>                     |      0 |               16 |                8 |             2000 |       5 |          8 |                   0 |                  1 |                     |                  7 | <NA>                       |                           |             0 |                    |                           |                        | <NA>              | <NA>                            |                                   |                            |                     nan |                               nan | <NA>                       |                           nan |                          nan | <NA>                                 |                         |                              |                                               |                                     |                          |                                          |                   nan |            nan |                      nan |             nan |            nan |                               nan |                            nan |                         nan |                                   | <NA>                                |                    |                   |                    nan |                         |                                  nan |                                            nan |                                        nan |                                                  nan |                                            nan |                                         nan |                                      nan |                                 nan |                                nan |                         nan |                        nan |                          nan |                         nan |
|  2005 |           1 |      16 | AP         | 200516000013013 |                      0 |                1 |       3 |                    3 |                  3 | <NA>                     |      1 |               30 |                4 |             2000 |       5 |          2 |                   0 |                  1 |                     |                  7 | <NA>                       |                           |             0 |                    |                           |                        | <NA>              | <NA>                            |                                   |                            |                     nan |                               nan | <NA>                       |                           nan |                          nan | <NA>                                 |                         |                              |                                               |                                     |                          |                                          |                   nan |            nan |                      nan |             nan |            nan |                               nan |                            nan |                         nan |                                   | <NA>                                |                    |                   |                    nan |                         |                                  nan |                                            nan |                                        nan |                                                  nan |                                            nan |                                         nan |                                      nan |                                 nan |                                nan |                         nan |                        nan |                          nan |                         nan |
|  2005 |           1 |      16 | AP         | 200516000013014 |                      0 |                1 |       7 |                    3 |                  3 | <NA>                     |      0 |                6 |                7 |             1997 |       8 |          8 |                   1 |                  1 |                   2 |                  1 | <NA>                       |                           |             1 |                    |                           |                        | <NA>              | <NA>                            |                                   |                            |                     nan |                               nan | <NA>                       |                           nan |                          nan | <NA>                                 |                         |                              |                                               |                                     |                          |                                          |                   nan |            nan |                      nan |             nan |            nan |                               nan |                            nan |                         nan |                                   | <NA>                                |                    |                   |                    nan |                         |                                  nan |                                            nan |                                        nan |                                                  nan |                                            nan |                                         nan |                                      nan |                                 nan |                                nan |                         nan |                        nan |                          nan |                         nan |
|  2005 |           1 |      16 | AP         | 200516000013020 |                      0 |                1 |       3 |                    3 |                  3 | <NA>                     |      0 |               28 |                3 |             1999 |       6 |          8 |                   0 |                  1 |                     |                  7 | <NA>                       |                           |             0 |                    |                           |                        | <NA>              | <NA>                            |                                   |                            |                     nan |                               nan | <NA>                       |                           nan |                          nan | <NA>                                 |                         |                              |                                               |                                     |                          |                                          |                   nan |            nan |                      nan |             nan |            nan |                               nan |                            nan |                         nan |                                   | <NA>                                |                    |                   |                    nan |                         |                                  nan |                                            nan |                                        nan |                                                  nan |                                            nan |                                         nan |                                      nan |                                 nan |                                nan |                         nan |                        nan |                          nan |                         nan |
|  2005 |           1 |      16 | AP         | 200516000013025 |                      0 |                1 |       2 |                    4 |                  4 | <NA>                     |      0 |               14 |               10 |             1997 |       7 |          8 |                   1 |                  1 |                   1 |                  1 | <NA>                       |                           |             0 |                    |                           |                        | <NA>              | <NA>                            |                                   |                            |                     nan |                               nan | <NA>                       |                           nan |                          nan | <NA>                                 |                         |                              |                                               |                                     |                          |                                          |                   nan |            nan |                      nan |             nan |            nan |                               nan |                            nan |                         nan |                                   | <NA>                                |                    |                   |                    nan |                         |                                  nan |                                            nan |                                        nan |                                                  nan |                                            nan |                                         nan |                                      nan |                                 nan |                                nan |                         nan |                        nan |                          nan |                         nan |

---
