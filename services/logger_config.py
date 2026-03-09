"""
Configuração central de logs do projeto.

Este módulo cria um logger simples que grava mensagens em arquivo
("logs/app.log") e também mostra as mensagens no terminal.
"""

from __future__ import annotations

import logging
from pathlib import Path


# Pasta de logs do projeto.
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

# Arquivo principal de log.
LOG_FILE = LOG_DIR / "app.log"


def get_logger(nome: str = "importador_excel") -> logging.Logger:
    """
    Retorna um logger configurado.

    Regras importantes:
    - cria a pasta de logs automaticamente, se necessário;
    - evita adicionar handlers repetidos;
    - grava no arquivo e também no console.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(nome)
    logger.setLevel(logging.INFO)

    # Se o logger já estiver configurado, apenas retorna.
    if logger.handlers:
        return logger

    # Formato padrão para deixar o log legível.
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Handler para arquivo.
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Handler para terminal.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
