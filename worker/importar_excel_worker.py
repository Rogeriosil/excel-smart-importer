"""
Worker simples para importar uma planilha para a API.

Uso:
1. Rode a API Flask.
2. Coloque um arquivo Excel em uma pasta conhecida.
3. Execute este script passando o caminho do arquivo.

Exemplo:
python importar_excel_worker.py ../arquivos_exemplo/clientes_exemplo.xlsx
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


def main() -> None:
    """
    Ponto de entrada do worker.
    """
    load_dotenv()

    if len(sys.argv) < 2:
        print("Uso: python importar_excel_worker.py CAMINHO_DO_ARQUIVO.xlsx")
        raise SystemExit(1)

    caminho = Path(sys.argv[1])
    if not caminho.exists():
        print(f"Arquivo não encontrado: {caminho}")
        raise SystemExit(1)

    api_base = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
    url = f"{api_base}/api/importar"

    with caminho.open("rb") as arquivo:
        resposta = requests.post(
            url,
            files={"arquivo": (caminho.name, arquivo, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            timeout=60,
        )

    print("Status HTTP:", resposta.status_code)
    print("Resposta da API:")
    print(resposta.text)


if __name__ == "__main__":
    main()
