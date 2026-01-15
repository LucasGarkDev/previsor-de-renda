"ml_pipeline/src/utils/logging.py"
"""
Configuração central de logging do pipeline
"""

import logging
from pathlib import Path

from ml_pipeline.src.config.settings import PROJECT_ROOT


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado para o projeto.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Log para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Log para arquivo (opcional)
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(logs_dir / "pipeline.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
