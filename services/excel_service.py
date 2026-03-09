"""
Serviço principal de importação do Excel.

Responsabilidades:
- ler o arquivo XLSX com pandas;
- validar se as colunas mínimas existem;
- limpar os dados;
- separar linhas válidas e inválidas;
- persistir tudo no banco.
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd

from models import ClienteImportado, ErroImportacao, Importacao, db
from services.logger_config import get_logger
from services.validators import (
    erro_primeiro_campo_invalido,
    limpar_texto,
    somente_digitos,
)


logger = get_logger(__name__)


# Colunas mínimas exigidas pelo projeto.
COLUNAS_OBRIGATORIAS = ["nome", "documento", "email", "telefone"]


def normalizar_nomes_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza os nomes das colunas para minúsculas sem espaços extras.
    """
    df.columns = [str(col).strip().lower() for col in df.columns]
    return df


def validar_colunas(df: pd.DataFrame) -> list[str]:
    """
    Retorna uma lista com colunas ausentes.
    """
    faltantes = [col for col in COLUNAS_OBRIGATORIAS if col not in df.columns]
    return faltantes


def processar_arquivo_excel(arquivo: BinaryIO, nome_arquivo: str) -> dict:
    """
    Processa um arquivo Excel enviado pela API.

    Fluxo geral:
    1. lê o XLSX;
    2. valida colunas;
    3. cria o registro de importação;
    4. percorre linha a linha;
    5. salva válidos e inválidos;
    6. devolve um resumo.
    """
    logger.info("Iniciando importação do arquivo: %s", nome_arquivo)

    # Lê o Excel em memória.
    df = pd.read_excel(arquivo)
    df = normalizar_nomes_colunas(df)

    faltantes = validar_colunas(df)
    if faltantes:
        msg = f"Colunas obrigatórias ausentes: {', '.join(faltantes)}"
        logger.warning(msg)
        raise ValueError(msg)

    # Cria o cabeçalho da importação.
    importacao = Importacao(
        nome_arquivo=nome_arquivo,
        total_linhas=len(df),
        total_validas=0,
        total_invalidas=0,
    )
    db.session.add(importacao)
    db.session.flush()

    # Itera sobre as linhas da planilha.
    # O +2 é usado porque a linha 1 costuma ser o cabeçalho do Excel.
    for indice, row in df.iterrows():
        linha_excel = indice + 2

        nome = limpar_texto(row.get("nome"))
        documento = somente_digitos(row.get("documento"))
        email = limpar_texto(row.get("email"))
        telefone = somente_digitos(row.get("telefone"))

        motivo_erro = erro_primeiro_campo_invalido(
            nome=nome,
            documento=documento,
            email=email,
            telefone=telefone,
        )

        if motivo_erro:
            erro = ErroImportacao(
                importacao_id=importacao.id,
                linha_excel=linha_excel,
                nome=nome,
                documento=documento,
                email=email,
                telefone=telefone,
                motivo=motivo_erro,
            )
            db.session.add(erro)
            importacao.total_invalidas += 1
            continue

        cliente = ClienteImportado(
            importacao_id=importacao.id,
            linha_excel=linha_excel,
            nome=nome,
            documento=documento,
            email=email or None,
            telefone=telefone or None,
            status="importado",
        )
        db.session.add(cliente)
        importacao.total_validas += 1

    db.session.commit()
    logger.info(
        "Importação concluída | arquivo=%s | válidas=%s | inválidas=%s",
        nome_arquivo,
        importacao.total_validas,
        importacao.total_invalidas,
    )

    return {
        "mensagem": "Importação concluída com sucesso.",
        "importacao": importacao.to_dict(),
    }


def processar_caminho_excel(caminho: str | Path) -> dict:
    """
    Função auxiliar para o worker em linha de comando.
    """
    caminho = Path(caminho)
    with caminho.open("rb") as arquivo:
        return processar_arquivo_excel(arquivo=arquivo, nome_arquivo=caminho.name)
