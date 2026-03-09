"""
Funções de validação e limpeza de dados.

Este módulo concentra regras simples de negócio para o importador.
A ideia é separar responsabilidades:
- leitura do Excel em um módulo;
- validação e limpeza neste módulo.
"""

from __future__ import annotations

import re
from typing import Optional


# Expressão simples para validar e-mail.
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def limpar_texto(valor: object) -> str:
    """
    Converte qualquer valor em string limpa.

    Regras:
    - None vira string vazia;
    - remove espaços nas pontas;
    - reduz espaços duplicados no meio.
    """
    if valor is None:
        return ""

    texto = str(valor).strip()

    # Junta espaços duplicados para melhorar a qualidade do dado.
    return " ".join(texto.split())


def somente_digitos(valor: object) -> str:
    """
    Remove tudo que não for número.

    Exemplo:
    '123.456.789-00' -> '12345678900'
    """
    return re.sub(r"\D", "", limpar_texto(valor))


def validar_email(email: str) -> bool:
    """
    Valida o formato básico do e-mail.

    Observação:
    - e-mail vazio é aceito como opcional;
    - se vier preenchido, precisa respeitar o padrão mínimo.
    """
    email = limpar_texto(email)
    if not email:
        return True
    return bool(EMAIL_RE.match(email))


def validar_documento(documento: str) -> bool:
    """
    Valida um documento simples (CPF/CNPJ) apenas pelo tamanho.

    Regras:
    - CPF: 11 dígitos
    - CNPJ: 14 dígitos

    Observação importante:
    Esta validação não calcula dígitos verificadores.
    O objetivo aqui é manter o projeto júnior forte e didático.
    """
    documento = somente_digitos(documento)
    return len(documento) in {11, 14}


def validar_nome(nome: str) -> bool:
    """
    Garante que o nome tenha conteúdo útil.
    """
    nome = limpar_texto(nome)
    return len(nome) >= 3


def validar_telefone(telefone: str) -> bool:
    """
    Aceita telefone vazio ou com tamanho razoável.
    """
    telefone = somente_digitos(telefone)
    if not telefone:
        return True
    return 10 <= len(telefone) <= 13


def erro_primeiro_campo_invalido(
    nome: str,
    documento: str,
    email: str,
    telefone: str,
) -> Optional[str]:
    """
    Retorna a primeira mensagem de erro encontrada.

    Isso ajuda a mostrar para o usuário exatamente o motivo da rejeição.
    """
    if not validar_nome(nome):
        return "Nome inválido. Informe pelo menos 3 caracteres."

    if not validar_documento(documento):
        return "Documento inválido. Use CPF (11 dígitos) ou CNPJ (14 dígitos)."

    if not validar_email(email):
        return "E-mail inválido."

    if not validar_telefone(telefone):
        return "Telefone inválido."

    return None
