# ml_pipeline/src/models/evaluate_all_models_v2.py

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from catboost import CatBoostRegressor

from ml_pipeline.src.utils.io import read_parquet


DATA_PATH = Path("data/processed/v3/test.parquet")
TARGET = "renda_mensal_ocupacao_principal_deflacionado"
MODELS_DIR = Path("models")


def compute_metrics(y_true, y_pred, y_true_log=None, y_pred_log=None):

    results = {}

    if y_true_log is not None:
        results["R2_log"] = r2_score(y_true_log, y_pred_log)
        results["RMSE_log"] = np.sqrt(mean_squared_error(y_true_log, y_pred_log))
        results["MAE_log"] = mean_absolute_error(y_true_log, y_pred_log)

    results["R2"] = r2_score(y_true, y_pred)
    results["RMSE"] = np.sqrt(mean_squared_error(y_true, y_pred))
    results["MAE"] = mean_absolute_error(y_true, y_pred)

    return results


def looks_like_log(values):
    """
    Heurística:
    Se média estiver entre 5 e 12, provavelmente é log.
    """
    mean_val = np.mean(values)
    return 5 < mean_val < 12


def evaluate_model(model_path, test):

    print(f"→ Avaliando {model_path.name}")

    y_true = test[TARGET]
    y_true_log = np.log(y_true)

    X = test.drop(columns=[TARGET, "id_domicilio"], errors="ignore").copy()

    # Limpeza categóricas
    cat_features = X.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in cat_features:
        X[col] = X[col].astype(str).fillna("MISSING")

    # ===============================
    # Carregar modelo
    # ===============================

    if model_path.suffix == ".cbm":
        model = CatBoostRegressor()
        model.load_model(model_path)
    else:
        model = joblib.load(model_path)

    # ===============================
    # Predição
    # ===============================
    try:
        y_pred_raw = model.predict(X)
    except:
        # Alguns modelos antigos podem precisar feature específica
        try:
            X_alt = test[model.feature_names_in_]
            y_pred_raw = model.predict(X_alt)
        except:
            print("⚠ Não foi possível avaliar:", model_path.name)
            return None

    # ===============================
    # Detectar se está em log
    # ===============================
    if looks_like_log(y_pred_raw):
        y_pred_log = y_pred_raw
        y_pred = np.exp(y_pred_log)
    else:
        y_pred = y_pred_raw
        y_pred_log = np.log(np.maximum(y_pred, 1))

    metrics = compute_metrics(y_true, y_pred, y_true_log, y_pred_log)
    metrics["Model"] = model_path.name

    return metrics


def evaluate_all():

    print("📊 Avaliando TODOS os modelos da pasta models\n")

    test = read_parquet(DATA_PATH)

    results = []

    for model_file in MODELS_DIR.iterdir():

        if model_file.suffix not in [".joblib", ".cbm", ".pkl"]:
            continue

        # Ignorar arquivos auxiliares
        if "smearing" in model_file.name:
            continue

        metrics = evaluate_model(model_file, test)

        if metrics is not None:
            results.append(metrics)

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values("R2", ascending=False)

    print("\n🏆 RANKING FINAL")
    print(df_results.round(4))


if __name__ == "__main__":
    evaluate_all()