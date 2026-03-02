# ml_pipeline/src/debug/check_columns_v3.py

from pathlib import Path
import pandas as pd

from ml_pipeline.src.utils.io import read_parquet


def check_columns():

    print("\n🔎 DIAGNÓSTICO DE COLUNAS — V3\n")

    train_path = Path("data/processed/v3/train.parquet")
    val_path   = Path("data/processed/v3/validation.parquet")
    test_path  = Path("data/processed/v3/test.parquet")

    train = read_parquet(train_path)
    val   = read_parquet(val_path)
    test  = read_parquet(test_path)

    print("📊 TRAIN COLUMNS:")
    print(sorted(train.columns.tolist()))
    print(f"\nTotal: {len(train.columns)} colunas\n")

    print("📊 VALIDATION COLUMNS:")
    print(sorted(val.columns.tolist()))
    print(f"\nTotal: {len(val.columns)} colunas\n")

    print("📊 TEST COLUMNS:")
    print(sorted(test.columns.tolist()))
    print(f"\nTotal: {len(test.columns)} colunas\n")

    print("🔎 Checando presença de colunas estruturais importantes:\n")

    expected = [
        "idade",
        "anos_estudo",
        "experiencia",
        "experiencia_squared",
        "renda_mensal_ocupacao_principal_deflacionado"
    ]

    for col in expected:
        print(f"{col}: {'✅ EXISTE' if col in train.columns else '❌ NÃO EXISTE'}")


if __name__ == "__main__":
    check_columns()