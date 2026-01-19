# ml_pipeline/src/models/evaluate_model_v2.py
"""
Avaliação final dos modelos V2 no conjunto de TESTE
(TEST SET EVALUATION — GENERALIZAÇÃO)
"""

import joblib
from pathlib import Path

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from ml_pipeline.src.config.settings import (
    DATA_PROCESSED_DIR,
    TARGET_COLUMN,
)
from ml_pipeline.src.utils.io import read_parquet
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)


def evaluate_model_v2(model_name: str):
    logger.info(f"Iniciando avaliação FINAL do modelo V2: {model_name}")

    # =========================
    # Caminhos
    # =========================
    model_path = Path("models") / f"{model_name}.joblib"
    test_path = DATA_PROCESSED_DIR / "v2" / "test.parquet"

    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

    # =========================
    # Leitura dos dados
    # =========================
    df_test = read_parquet(test_path)

    X_test = df_test.drop(columns=[TARGET_COLUMN])
    y_test = df_test[TARGET_COLUMN]

    # =========================
    # AJUSTE ESTRUTURAL (CRÍTICO)
    # =========================
    if model_name == "catboost_v2_no_id":
        if "id_domicilio" in X_test.columns:
            logger.warning(
                "Removendo coluna 'id_domicilio' do TESTE "
                "para compatibilidade com catboost_v2_no_id"
            )
            X_test = X_test.drop(columns=["id_domicilio"])

    # =========================
    # Tratamento de categóricas
    # =========================
    categorical_features = X_test.select_dtypes(
        include=["object"]
    ).columns.tolist()

    logger.info(
        f"Tratando colunas categóricas no TESTE ({len(categorical_features)}): "
        f"{categorical_features}"
    )

    for col in categorical_features:
        X_test[col] = X_test[col].fillna("MISSING")

    # =========================
    # Carregar modelo
    # =========================
    model = joblib.load(model_path)

    # =========================
    # Predição
    # =========================
    preds = model.predict(X_test)

    # =========================
    # Métricas
    # =========================
    rmse = mean_squared_error(y_test, preds) ** 0.5
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    # =========================
    # Logs finais
    # =========================
    logger.info(f"[TESTE V2] {model_name}")
    logger.info(f"RMSE: {rmse:.4f}")
    logger.info(f"MAE : {mae:.4f}")
    logger.info(f"R²  : {r2:.4f}")

    return {
        "model": model_name,
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }


if __name__ == "__main__":
    evaluate_model_v2("catboost_v2")
    evaluate_model_v2("catboost_v2_no_id")
