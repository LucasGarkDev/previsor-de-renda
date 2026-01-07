"""
Engenharia de atributos para o modelo
"""

import pandas as pd
import numpy as np

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
    APPLY_LOG_TARGET
)


def build_features():
    input_path = DATA_PROCESSED_DIR / "pnad_transformed.parquet"
    df = pd.read_parquet(input_path)

    # Feature: idade ao quadrado
    df["idade_squared"] = df["idade"] ** 2

    # Log da renda (se configurado)
    if APPLY_LOG_TARGET:
        df[f"log_{TARGET_COLUMN}"] = np.log(df[TARGET_COLUMN])

    output_path = DATA_PROCESSED_DIR / "train_ready.parquet"
    df.to_parquet(output_path, index=False)

    print("Engenharia de atributos concluída")
    print(f"Arquivo salvo em: {output_path}")

    return output_path


if __name__ == "__main__":
    build_features()
