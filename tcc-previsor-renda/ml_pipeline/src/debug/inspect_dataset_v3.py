# ml_pipeline/src/debug/inspect_dataset_v3.py

import pandas as pd


def inspect_dataset(path: str):
    print(f"\n🔎 Inspecionando dataset: {path}\n")

    df = pd.read_parquet(path)

    print("📌 Shape:")
    print(df.shape)

    print("\n📌 Colunas:")
    print(df.columns.tolist())

    print("\n📌 Tipos:")
    print(df.dtypes)

    print("\n📌 Primeiras 5 linhas:")
    print(df.head())

    print("\n📌 Valores nulos por coluna:")
    print(df.isnull().sum().sort_values(ascending=False))

    # Verificações específicas
    required_columns = [
        "renda_mensal_ocupacao_principal_deflacionado",
        "log_renda",
        "anos_estudo",
        "idade",
        "sexo",
        "possui_carteira_assinada",
        "regiao",
    ]

    print("\n📌 Checando colunas necessárias para Mincer:")
    for col in required_columns:
        if col in df.columns:
            print(f"✅ {col} — OK")
        else:
            print(f"❌ {col} — NÃO ENCONTRADA")


if __name__ == "__main__":
    inspect_dataset("data/processed/v3/train.parquet")