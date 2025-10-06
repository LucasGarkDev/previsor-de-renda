from google.cloud import bigquery
from pathlib import Path

def detectar_coluna_uf(client: bigquery.Client) -> str | None:
    sql = """
    SELECT column_name
    FROM `basedosdados.br_ibge_pnadc.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'microdados'
      AND REGEXP_CONTAINS(column_name, r'(?i)uf|sigla')
    ORDER BY column_name
    """
    cols = client.query(sql).result().to_dataframe()["column_name"].str.strip().tolist()
    for candidato in ("sigla_uf", "uf", "UF", "siglaUF", "SIGLA_UF"):
        if candidato in cols:
            return candidato
    return None

def get_pnad_sample(client: bigquery.Client, uf_col: str | None):
    uf_select = f", {uf_col} AS uf" if uf_col else ""
    query = f"""
    SELECT
      ano
      {uf_select},
      V2007 AS sexo,
      V2010 AS cor,
      V2009 AS idade,
      V3009 AS escolaridade,
      V4010 AS ocupacao,
      V4048 AS jornada,
      V4012 AS posicao,
      habitual AS renda
    FROM `basedosdados.br_ibge_pnadc.microdados`
    WHERE ano = 2022
    LIMIT 1000
    """
    return client.query(query).result().to_dataframe()

if __name__ == "__main__":
    client = bigquery.Client()

    uf_col = detectar_coluna_uf(client)
    if uf_col:
        print(f"[INFO] Coluna de UF detectada: {uf_col}")
    else:
        print("[WARN] Nenhuma coluna de UF detectada. Prosseguindo sem UF...")

    df = get_pnad_sample(client, uf_col)
    print(df.head())

    Path("data/raw").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/raw/pnad_2022_sample.csv", index=False)
    print("✅ Amostra salva em data/raw/pnad_2022_sample.csv")
