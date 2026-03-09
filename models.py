"""
Modelos do banco de dados do projeto.

Este arquivo define as tabelas principais:
- Importacao: cabeçalho da importação;
- ClienteImportado: linhas válidas importadas;
- ErroImportacao: linhas inválidas rejeitadas.
"""

from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


# Instância global do SQLAlchemy.
# Ela será iniciada no app.py.
db = SQLAlchemy()


class Importacao(db.Model):
    """
    Representa uma importação de Excel.

    Guarda informações gerais do arquivo processado.
    """

    __tablename__ = "importacoes"

    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    total_linhas = db.Column(db.Integer, nullable=False, default=0)
    total_validas = db.Column(db.Integer, nullable=False, default=0)
    total_invalidas = db.Column(db.Integer, nullable=False, default=0)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    clientes = db.relationship(
        "ClienteImportado",
        backref="importacao",
        cascade="all, delete-orphan",
        lazy=True,
    )
    erros = db.relationship(
        "ErroImportacao",
        backref="importacao",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self) -> dict:
        """
        Converte o modelo em dicionário para resposta da API.
        """
        return {
            "id": self.id,
            "nome_arquivo": self.nome_arquivo,
            "total_linhas": self.total_linhas,
            "total_validas": self.total_validas,
            "total_invalidas": self.total_invalidas,
            "criado_em": self.criado_em.isoformat(),
        }


class ClienteImportado(db.Model):
    """
    Linhas válidas da planilha que passaram nas regras.
    """

    __tablename__ = "clientes_importados"

    id = db.Column(db.Integer, primary_key=True)
    importacao_id = db.Column(db.Integer, db.ForeignKey("importacoes.id"), nullable=False)
    linha_excel = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    documento = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="importado")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "importacao_id": self.importacao_id,
            "linha_excel": self.linha_excel,
            "nome": self.nome,
            "documento": self.documento,
            "email": self.email,
            "telefone": self.telefone,
            "status": self.status,
        }


class ErroImportacao(db.Model):
    """
    Linhas rejeitadas durante a importação.
    """

    __tablename__ = "erros_importacao"

    id = db.Column(db.Integer, primary_key=True)
    importacao_id = db.Column(db.Integer, db.ForeignKey("importacoes.id"), nullable=False)
    linha_excel = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(255), nullable=True)
    documento = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    motivo = db.Column(db.String(255), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "importacao_id": self.importacao_id,
            "linha_excel": self.linha_excel,
            "nome": self.nome,
            "documento": self.documento,
            "email": self.email,
            "telefone": self.telefone,
            "motivo": self.motivo,
        }
