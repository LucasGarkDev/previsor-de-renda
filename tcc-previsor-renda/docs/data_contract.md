# Contrato de Dados – Projeto Previsor de Renda

## Bases de dados

### Base principal
- PNAD tradicional (`br_ibge_pnad`)

### Bases auxiliares
- PNADC (`br_ibge_pnadc`)
- RAIS (`br_me_rais`)

## Variável alvo
- renda_mensal_ocupacao_principal_deflacionada

## Variáveis explicativas

### Capital humano
- anos_estudo
- ultimo_grau_frequentado
- sabe_ler_escrever

### Experiência
- idade

### Demografia
- sexo
- raca_cor

### Inserção no mercado de trabalho
- trabalhou_semana
- ocupacao_semana
- atividade_ramo_negocio_semana
- posicao_ocupacao
- possui_carteira_assinada
- horas_trabalhadas_semana

### Contexto geográfico
- sigla_uf
- regiao
- zona_urbana
- regiao_metropolitana

## Variáveis excluídas
- renda domiciliar como feature
- bens do domicílio
- transferências sociais

## Observações finais
Este contrato de dados formaliza as decisões metodológicas do projeto.
Alterações futuras devem ser explicitamente documentadas.