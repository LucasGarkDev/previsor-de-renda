from ml_pipeline.src.models.train2 import train_catboost
from ml_pipeline.src.utils.logging import get_logger

logger = get_logger(__name__)

PARAMS = [
    {"depth": 6, "learning_rate": 0.05},
    {"depth": 8, "learning_rate": 0.05},   # baseline atual
    {"depth": 10, "learning_rate": 0.05},
    {"depth": 8, "learning_rate": 0.03},
    {"depth": 8, "learning_rate": 0.07},
    {"depth": 6, "learning_rate": 0.03},
]


def run_tuning():
    results = []
    best_r2 = -float("inf")

    logger.info("=" * 80)
    logger.info("INICIANDO TUNING LEVE DO CATBOOST")
    logger.info(f"Total de configurações: {len(PARAMS)}")
    logger.info("=" * 80)

    for i, params in enumerate(PARAMS, start=1):
        logger.info("-" * 80)
        logger.info(
            f"Rodada {i}/{len(PARAMS)} | "
            f"depth={params['depth']} | "
            f"learning_rate={params['learning_rate']}"
        )

        metrics = train_catboost(
            depth=params["depth"],
            learning_rate=params["learning_rate"],
            save_suffix=f"d{params['depth']}_lr{params['learning_rate']}",
        )

        rmse = metrics["rmse"]
        mae = metrics["mae"]
        r2 = metrics["r2"]

        logger.info(
            f"Resultado | RMSE={rmse:.4f} | MAE={mae:.4f} | R²={r2:.4f}"
        )

        # Comparação incremental
        if r2 > best_r2:
            best_r2 = r2
            logger.info(">>> NOVO MELHOR MODELO ATÉ AGORA <<<")

        results.append({
            "depth": params["depth"],
            "learning_rate": params["learning_rate"],
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
        })

    # =========================
    # Resumo final
    # =========================
    logger.info("=" * 80)
    logger.info("RESUMO FINAL DO TUNING (ordenado por R²)")
    logger.info("=" * 80)

    results_sorted = sorted(results, key=lambda x: x["r2"], reverse=True)

    for res in results_sorted:
        logger.info(
            f"depth={res['depth']} | "
            f"lr={res['learning_rate']} | "
            f"RMSE={res['rmse']:.4f} | "
            f"MAE={res['mae']:.4f} | "
            f"R²={res['r2']:.4f}"
        )

    logger.info("=" * 80)
    logger.info("TUNING FINALIZADO")
    logger.info("=" * 80)

    return results_sorted


if __name__ == "__main__":
    run_tuning()
