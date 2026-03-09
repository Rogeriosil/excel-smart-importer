"""
Aplicação principal do projeto Importador Inteligente de Excel.

Este projeto foi pensado para portfólio:
- API Flask;
- upload de Excel;
- validação de dados;
- persistência em SQLite;
- painel web simples para acompanhar importações.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

from models import Importacao, db
from services.excel_service import processar_arquivo_excel
from services.logger_config import get_logger


logger = get_logger(__name__)


def create_app() -> Flask:
    """
    Cria e configura a aplicação Flask.
    """
    load_dotenv()

    app = Flask(__name__, static_folder="web/static", template_folder="web")

    # Configurações principais.
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///importador_inteligente.sqlite3",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

    db.init_app(app)

    # Garante criação do banco na primeira execução.
    with app.app_context():
        db.create_all()

    @app.get("/")
    def home():
        """
        Entrega a interface web principal.
        """
        return send_from_directory("web", "index.html")

    @app.get("/static/<path:filename>")
    def static_files(filename: str):
        """
        Entrega arquivos estáticos do frontend simples.
        """
        return send_from_directory("web/static", filename)

    @app.get("/api")
    def status_api():
        """
        Endpoint simples de saúde da API.
        """
        return jsonify({
            "status": "ok",
            "projeto": "Importador Inteligente de Excel",
        })

    @app.post("/api/importar")
    def importar_excel():
        """
        Recebe um arquivo Excel e dispara a importação.
        """
        arquivo = request.files.get("arquivo")

        if not arquivo:
            return jsonify({"erro": "Envie um arquivo Excel no campo 'arquivo'."}), 400

        if not arquivo.filename.lower().endswith((".xlsx", ".xls")):
            return jsonify({"erro": "Arquivo inválido. Envie um Excel (.xlsx ou .xls)."}), 400

        try:
            resultado = processar_arquivo_excel(arquivo, arquivo.filename)
            return jsonify(resultado), 201
        except ValueError as exc:
            logger.warning("Erro de validação na importação: %s", exc)
            return jsonify({"erro": str(exc)}), 400
        except Exception as exc:  # noqa: BLE001
            logger.exception("Erro inesperado na importação")
            return jsonify({"erro": f"Erro inesperado: {exc}"}), 500

    @app.get("/api/importacoes")
    def listar_importacoes():
        """
        Lista as importações mais recentes.
        """
        importacoes = Importacao.query.order_by(Importacao.id.desc()).all()
        return jsonify([item.to_dict() for item in importacoes])

    @app.get("/api/importacoes/<int:importacao_id>")
    def detalhes_importacao(importacao_id: int):
        """
        Retorna cabeçalho, válidos e inválidos de uma importação.
        """
        importacao = Importacao.query.get_or_404(importacao_id)
        return jsonify({
            "importacao": importacao.to_dict(),
            "validos": [item.to_dict() for item in importacao.clientes],
            "invalidos": [item.to_dict() for item in importacao.erros],
        })

    return app


app = create_app()


if __name__ == "__main__":
    # Modo de desenvolvimento.
    app.run(debug=True)
