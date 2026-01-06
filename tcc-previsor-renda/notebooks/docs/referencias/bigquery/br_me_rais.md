# Dataset `br_me_rais`

## Tabela `dicionario`

**Descrição:** Dicionário para tradução dos códigos do conjunto br_me_rais. Para taduzir códigos compartilhados entre instituições, como id_municipio, buscar por diretórios

- Linhas aproximadas: 6887
- Tamanho aproximado (MB): 0.5

### Esquema de colunas

| Coluna | Tipo | Modo | Descrição |
|--------|------|------|-----------|
| id_tabela | STRING | NULLABLE | ID Tabela |
| nome_coluna | STRING | NULLABLE | Nome da coluna |
| chave | STRING | NULLABLE | Chave |
| cobertura_temporal | STRING | NULLABLE | Cobertura Temporal |
| valor | STRING | NULLABLE | Valor |

### Exemplo de dados (5 linhas)

| id_tabela           | nome_coluna   |   chave | cobertura_temporal   | valor                                           |
|:--------------------|:--------------|--------:|:---------------------|:------------------------------------------------|
| microdados_vinculos | sexo          |       1 | (1)                  | Masculino                                       |
| microdados_vinculos | sexo          |       9 | (1)                  | Código não encontrado nos dicionários oficiais. |
| microdados_vinculos | sexo          |       2 | (1)                  | Feminino                                        |
| microdados_vinculos | sexo          |      -1 | (1)                  | Ignorado                                        |
| microdados_vinculos | raca_cor      |      99 | 2023                 | Código não encontrado nos dicionários oficiais. |

---

## Tabela `microdados_estabelecimentos`

**Descrição:** Microdados de estabelecimentos da RAIS.

- Linhas aproximadas: 230908897
- Tamanho aproximado (MB): 25461.07

### Esquema de colunas

| Coluna | Tipo | Modo | Descrição |
|--------|------|------|-----------|
| ano | INTEGER | NULLABLE | Ano |
| sigla_uf | STRING | NULLABLE | Sigla da Unidade da Federação |
| id_municipio | STRING | NULLABLE | ID Município - IBGE 7 Dígitos |
| quantidade_vinculos_ativos | INTEGER | NULLABLE | Estoque de vínculos ativos em 31/12. |
| quantidade_vinculos_clt | INTEGER | NULLABLE | Estoque de vínculos, sob o regime CLT e Outros, ativos em 31/12 |
| quantidade_vinculos_estatutarios | INTEGER | NULLABLE | Estoque de vínculos, sob o regime estatutário, ativos em 31/12 |
| natureza_estabelecimento | STRING | NULLABLE | Natureza do Estabelecimento |
| natureza_juridica | STRING | NULLABLE | Natureza jurídica (CONCLA/2002) |
| tamanho_estabelecimento | STRING | NULLABLE | Tamanho - empregados ativos em 31/12. |
| tipo_estabelecimento | STRING | NULLABLE | Tipo do Estabelecimento |
| indicador_cei_vinculado | INTEGER | NULLABLE | Indicador CEI Vinculado |
| indicador_pat | INTEGER | NULLABLE | Indicador de estabelecimento pertencente ao PAT. |
| indicador_simples | STRING | NULLABLE | Indicador de optante pelo SIMPLES. |
| indicador_rais_negativa | INTEGER | NULLABLE | Indicador de RAIS negativa. |
| indicador_atividade_ano | INTEGER | NULLABLE | Indicador de estabelecimento/entidade que exerceu atividade durante o ano de referência. |
| cnae_1 | STRING | NULLABLE | Código Nacional de Atividades Econômicas 1.0 |
| cnae_2 | STRING | NULLABLE | Código Nacional de Atividades Econômicas 2. |
| cnae_2_subclasse | STRING | NULLABLE | Subclasse do Código Nacional de Atividades Econômicas 2.0 |
| subsetor_ibge | STRING | NULLABLE | Subsetor IBGE |
| subatividade_ibge | STRING | NULLABLE | Subatividade IBGE |
| cep | STRING | NULLABLE | Código de Endereçamento Postal |
| bairros_sp | STRING | NULLABLE | Bairros do Municipio de São Paulo |
| distritos_sp | STRING | NULLABLE | Distritos do município de São Paulo |
| bairros_fortaleza | STRING | NULLABLE | Bairros do município de Fortaleza |
| bairros_rj | STRING | NULLABLE | Bairros do município do Rio de Janeiro |
| regioes_administrativas_df | STRING | NULLABLE | Regiões Administrativas do Distrito Federal |

### Exemplo de dados (5 linhas)

|   ano | sigla_uf   |   id_municipio |   quantidade_vinculos_ativos |   quantidade_vinculos_clt |   quantidade_vinculos_estatutarios | natureza_estabelecimento   |   natureza_juridica |   tamanho_estabelecimento |   tipo_estabelecimento |   indicador_cei_vinculado |   indicador_pat |   indicador_simples |   indicador_rais_negativa | indicador_atividade_ano   |   cnae_1 | cnae_2   | cnae_2_subclasse   | subsetor_ibge   | subatividade_ibge   | cep   | bairros_sp   | distritos_sp   | bairros_fortaleza   |   bairros_rj | regioes_administrativas_df   |
|------:|:-----------|---------------:|-----------------------------:|--------------------------:|-----------------------------------:|:---------------------------|--------------------:|--------------------------:|-----------------------:|--------------------------:|----------------:|--------------------:|--------------------------:|:--------------------------|---------:|:---------|:-------------------|:----------------|:--------------------|:------|:-------------|:---------------|:--------------------|-------------:|:-----------------------------|
|  2001 | RS         |        4317301 |                            0 |                         0 |                                  0 |                            |                2062 |                         0 |                      1 |                         0 |               0 |                   1 |                         1 | <NA>                      |    01112 |          |                    | AGRICULTURA     |                     |       |              |                |                     |           56 |                              |
|  2001 | RS         |        4315305 |                            0 |                         0 |                                  0 |                            |                2054 |                         0 |                      1 |                         0 |               0 |                   0 |                         1 | <NA>                      |    01112 |          |                    | AGRICULTURA     |                     |       |              |                |                     |           56 |                              |
|  2001 | RS         |        4318101 |                            0 |                         0 |                                  0 |                            |                4049 |                         0 |                      3 |                         0 |               0 |                   0 |                         0 | <NA>                      |    01112 |          |                    | AGRICULTURA     |                     |       |              |                |                     |           56 |                              |
|  2001 | RS         |        4318903 |                            0 |                         0 |                                  0 |                            |                4049 |                         0 |                      3 |                         0 |               0 |                   0 |                         0 | <NA>                      |    01112 |          |                    | AGRICULTURA     |                     |       |              |                |                     |           56 |                              |
|  2001 | RS         |        4306601 |                            0 |                         0 |                                  0 |                            |                4049 |                         0 |                      3 |                         0 |               0 |                   0 |                         0 | <NA>                      |    01112 |          |                    | AGRICULTURA     |                     |       |              |                |                     |           56 |                              |

---

## Tabela `microdados_vinculos`

**Descrição:** Microdados públicos dos vínculos de emprego na RAIS. Base desidentificada, isto é, que não inclui identificadores únicos de linha. Cada linha representa um vínculo - por isso indicamos este como nível de observação mesmo que não conste como coluna.

- Linhas aproximadas: 2055501488
- Tamanho aproximado (MB): 410441.43

### Esquema de colunas

| Coluna | Tipo | Modo | Descrição |
|--------|------|------|-----------|
| ano | INTEGER | NULLABLE | Ano |
| sigla_uf | STRING | NULLABLE | Sigla da Unidade da Federação |
| id_municipio | STRING | NULLABLE | ID Município - IBGE 7 Dígitos |
| tipo_vinculo | STRING | NULLABLE | Tipo do Vínculo |
| vinculo_ativo_3112 | STRING | NULLABLE | Vínculo Ativo no dia 31/12 |
| tipo_admissao | STRING | NULLABLE | Tipo da Admissão |
| mes_admissao | INTEGER | NULLABLE | Mês de Admissão |
| mes_desligamento | INTEGER | NULLABLE | Mês de Desligamento |
| motivo_desligamento | STRING | NULLABLE | Motivo do Desligamento |
| causa_desligamento_1 | STRING | NULLABLE | Causa 1 do Desligamento |
| causa_desligamento_2 | STRING | NULLABLE | Causa 2 do Desligamento |
| causa_desligamento_3 | STRING | NULLABLE | Causa 3 do Desligamento |
| faixa_tempo_emprego | STRING | NULLABLE | Faixa Tempo Emprego |
| faixa_horas_contratadas | STRING | NULLABLE | Faixa Horas Contratadas |
| tempo_emprego | FLOAT | NULLABLE | Tempo Emprego |
| quantidade_horas_contratadas | INTEGER | NULLABLE | Quantidade de Horas Contratadas |
| id_municipio_trabalho | STRING | NULLABLE | ID Município de Trabalho |
| quantidade_dias_afastamento | INTEGER | NULLABLE | Quantidade de Dias sob Afastamento |
| indicador_cei_vinculado | STRING | NULLABLE | Indicador CEI Vinculado |
| indicador_trabalho_parcial | STRING | NULLABLE | Indicador Trabalho Parcial |
| indicador_trabalho_intermitente | STRING | NULLABLE | Indicador Trabalho Intermitente |
| faixa_remuneracao_media_sm | STRING | NULLABLE | Faixa Remuneração Média (Salários Mínimos) |
| valor_remuneracao_media_sm | FLOAT | NULLABLE | Valor da Remuneração Média (Salários Mínimos) |
| valor_remuneracao_media | FLOAT | NULLABLE | Valor da Remuneração Média (Nominal) |
| faixa_remuneracao_dezembro_sm | STRING | NULLABLE | Faixa Remuneração em Dezembro (Salários Mínimos) |
| valor_remuneracao_dezembro_sm | FLOAT | NULLABLE | Valor da Remuneração em Dezembro (Salários Mínimos) |
| valor_remuneracao_janeiro | FLOAT | NULLABLE | Valor da Remuneração em Janeiro (Nominal) |
| valor_remuneracao_fevereiro | FLOAT | NULLABLE | Valor da Remuneração em Fevereiro (Nominal) |
| valor_remuneracao_marco | FLOAT | NULLABLE | Valor da Remuneração em Março (Nominal) |
| valor_remuneracao_abril | FLOAT | NULLABLE | Valor da Remuneração em Abril (Nominal) |
| valor_remuneracao_maio | FLOAT | NULLABLE | Valor da Remuneração em Maio (Nominal) |
| valor_remuneracao_junho | FLOAT | NULLABLE | Valor da Remuneração em Junho (Nominal) |
| valor_remuneracao_julho | FLOAT | NULLABLE | Valor da Remuneração em Julho (Nominal) |
| valor_remuneracao_agosto | FLOAT | NULLABLE | Valor da Remuneração em Agosto (Nominal) |
| valor_remuneracao_setembro | FLOAT | NULLABLE | Valor da Remuneração em Setembro (Nominal) |
| valor_remuneracao_outubro | FLOAT | NULLABLE | Valor da Remuneração em Outubro (Nominal) |
| valor_remuneracao_novembro | FLOAT | NULLABLE | Valor da Remuneração em Novembro (Nominal) |
| valor_remuneracao_dezembro | FLOAT | NULLABLE | Valor da Remuneração em Dezembro (Nominal) |
| tipo_salario | STRING | NULLABLE | Tipo do Salário |
| valor_salario_contratual | FLOAT | NULLABLE | Valor Contratual do Salário |
| subatividade_ibge | STRING | NULLABLE | Subatividade - IBGE |
| subsetor_ibge | STRING | NULLABLE | Subsetor - IBGE |
| cbo_1994 | STRING | NULLABLE | Classificação Brasileira de Ocupações (CBO) 1994 |
| cbo_2002 | STRING | NULLABLE | Classificação Brasileira de Ocupações (CBO) 2002 |
| cnae_1 | STRING | NULLABLE | Classificação Nacional de Atividades Econômicas (CNAE) 1.0 |
| cnae_2 | STRING | NULLABLE | Classificação Nacional de Atividades Econômicas (CNAE) 2.0 |
| cnae_2_subclasse | STRING | NULLABLE | Classificação Nacional de Atividades Econômicas (CNAE) 2.0 Subclasse |
| faixa_etaria | STRING | NULLABLE | Faixa Etária |
| idade | INTEGER | NULLABLE | Idade |
| grau_instrucao_1985_2005 | STRING | NULLABLE | Grau de Instrução 1985-2005 |
| grau_instrucao_apos_2005 | STRING | NULLABLE | Grau de Instrução Após 2005 |
| nacionalidade | STRING | NULLABLE | Nacionalidade |
| sexo | STRING | NULLABLE | Sexo do Trabalhador |
| raca_cor | STRING | NULLABLE | Raça ou Cor |
| indicador_portador_deficiencia | STRING | NULLABLE | Indicador de Portador de Deficiência |
| tipo_deficiencia | STRING | NULLABLE | Tipo da Deficiência |
| ano_chegada_brasil | INTEGER | NULLABLE | Ano de Chegada no Brasil |
| tamanho_estabelecimento | STRING | NULLABLE | Tamanho do Estabelecimento |
| tipo_estabelecimento | STRING | NULLABLE | Tipo do Estabelecimento |
| natureza_juridica | STRING | NULLABLE | Natureza Jurídica |
| indicador_simples | STRING | NULLABLE | Indicador do Simples |
| bairros_sp | STRING | NULLABLE | Bairros em São Paulo |
| distritos_sp | STRING | NULLABLE | Distritos em São Paulo |
| bairros_fortaleza | STRING | NULLABLE | Bairros em Fortaleza |
| bairros_rj | STRING | NULLABLE | Bairros no Rio de Janeiro |
| regioes_administrativas_df | STRING | NULLABLE | Regiões Administrativas no Distrito Federal |

### Exemplo de dados (5 linhas)

|   ano | sigla_uf   |   id_municipio |   tipo_vinculo |   vinculo_ativo_3112 | tipo_admissao   | mes_admissao   | mes_desligamento   |   motivo_desligamento | causa_desligamento_1   | causa_desligamento_2   | causa_desligamento_3   |   faixa_tempo_emprego | faixa_horas_contratadas   |   tempo_emprego | quantidade_horas_contratadas   | id_municipio_trabalho   | quantidade_dias_afastamento   | indicador_cei_vinculado   | indicador_trabalho_parcial   | indicador_trabalho_intermitente   |   faixa_remuneracao_media_sm |   valor_remuneracao_media_sm |   valor_remuneracao_media | faixa_remuneracao_dezembro_sm   |   valor_remuneracao_dezembro_sm |   valor_remuneracao_janeiro |   valor_remuneracao_fevereiro |   valor_remuneracao_marco |   valor_remuneracao_abril |   valor_remuneracao_maio |   valor_remuneracao_junho |   valor_remuneracao_julho |   valor_remuneracao_agosto |   valor_remuneracao_setembro |   valor_remuneracao_outubro |   valor_remuneracao_novembro |   valor_remuneracao_dezembro | tipo_salario   |   valor_salario_contratual | subatividade_ibge   | subsetor_ibge   |   cbo_1994 | cbo_2002   | cnae_1   | cnae_2   | cnae_2_subclasse   |   faixa_etaria | idade   |   grau_instrucao_1985_2005 | grau_instrucao_apos_2005   |   nacionalidade |   sexo | raca_cor   | indicador_portador_deficiencia   | tipo_deficiencia   | ano_chegada_brasil   |   tamanho_estabelecimento | tipo_estabelecimento   | natureza_juridica   | indicador_simples   | bairros_sp   | distritos_sp   | bairros_fortaleza   | bairros_rj   | regioes_administrativas_df   |
|------:|:-----------|---------------:|---------------:|---------------------:|:----------------|:---------------|:-------------------|----------------------:|:-----------------------|:-----------------------|:-----------------------|----------------------:|:--------------------------|----------------:|:-------------------------------|:------------------------|:------------------------------|:--------------------------|:-----------------------------|:----------------------------------|-----------------------------:|-----------------------------:|--------------------------:|:--------------------------------|--------------------------------:|----------------------------:|------------------------------:|--------------------------:|--------------------------:|-------------------------:|--------------------------:|--------------------------:|---------------------------:|-----------------------------:|----------------------------:|-----------------------------:|-----------------------------:|:---------------|---------------------------:|:--------------------|:----------------|-----------:|:-----------|:---------|:---------|:-------------------|---------------:|:--------|---------------------------:|:---------------------------|----------------:|-------:|:-----------|:---------------------------------|:-------------------|:---------------------|--------------------------:|:-----------------------|:--------------------|:--------------------|:-------------|:---------------|:--------------------|:-------------|:-----------------------------|
|  1991 | RJ         |        3304300 |              1 |                    1 |                 | <NA>           | <NA>               |                       |                        |                        |                        |                     8 |                           |            12.5 | <NA>                           |                         | <NA>                          |                           |                              |                                   |                            1 |                         0.99 |                       nan |                                 |                               0 |                         nan |                           nan |                       nan |                       nan |                      nan |                       nan |                       nan |                        nan |                          nan |                         nan |                          nan |                          nan |                |                        nan |                     |                 |      63590 |            |          |          |                    |              6 | <NA>    |                          1 |                            |              10 |      1 |            |                                  |                    | <NA>                 |                         2 | Não identificado       |                     |                     |              |                |                     |              |                              |
|  1991 | RJ         |        3304201 |              1 |                    0 |                 | <NA>           | 1                  |                     4 |                        |                        |                        |                     6 |                           |             4.8 | <NA>                           |                         | <NA>                          |                           |                              |                                   |                            8 |                        12.38 |                       nan |                                 |                               0 |                         nan |                           nan |                       nan |                       nan |                      nan |                       nan |                       nan |                        nan |                          nan |                         nan |                          nan |                          nan |                |                        nan |                     |                 |      62190 |            |          |          |                    |              5 | <NA>    |                          1 |                            |              10 |      1 |            |                                  |                    | <NA>                 |                         5 | 3                      |                     |                     |              |                |                     |              |                              |
|  1991 | RJ         |        3304300 |              1 |                    0 |                 | <NA>           | 1                  |                     4 |                        |                        |                        |                     2 |                           |             0.4 | <NA>                           |                         | <NA>                          |                           |                              |                                   |                            2 |                         1    |                       nan |                                 |                               0 |                         nan |                           nan |                       nan |                       nan |                      nan |                       nan |                       nan |                        nan |                          nan |                         nan |                          nan |                          nan |                |                        nan |                     |                 |      63950 |            |          |          |                    |              3 | <NA>    |                          2 |                            |              10 |      1 |            |                                  |                    | <NA>                 |                         4 |                        |                     |                     |              |                |                     |              |                              |
|  1991 | RJ         |        3304300 |              1 |                    0 |                 | <NA>           | 1                  |                     4 |                        |                        |                        |                     2 |                           |             0.3 | <NA>                           |                         | <NA>                          |                           |                              |                                   |                            1 |                         0.99 |                       nan |                                 |                               0 |                         nan |                           nan |                       nan |                       nan |                      nan |                       nan |                       nan |                        nan |                          nan |                         nan |                          nan |                          nan |                |                        nan |                     |                 |      63950 |            |          |          |                    |              3 | <NA>    |                          2 |                            |              10 |      1 |            |                                  |                    | <NA>                 |                         4 |                        |                     |                     |              |                |                     |              |                              |
|  1991 | RJ         |        3304300 |              1 |                    0 |                 | <NA>           | 5                  |                     4 |                        |                        |                        |                     3 |                           |             0.7 | <NA>                           |                         | <NA>                          |                           |                              |                                   |                            2 |                         1    |                       nan |                                 |                               0 |                         nan |                           nan |                       nan |                       nan |                      nan |                       nan |                       nan |                        nan |                          nan |                         nan |                          nan |                          nan |                |                        nan |                     |                 |      63950 |            |          |          |                    |              3 | <NA>    |                          2 |                            |              10 |      1 |            |                                  |                    | <NA>                 |                         4 |                        |                     |                     |              |                |                     |              |                              |

---
