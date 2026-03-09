# Importador Inteligente de Excel

Projeto pensado para portfólio **júnior forte**.

Este sistema recebe um arquivo Excel, valida os dados, separa linhas válidas e inválidas, salva tudo em banco SQLite e exibe os resultados em um painel web simples.

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- pandas
- openpyxl
- SQLite
- HTML
- CSS
- JavaScript

## O que o projeto demonstra

- Upload de Excel pela web
- Validação de colunas obrigatórias
- Limpeza e normalização de dados
- Registro de erros por linha
- Persistência em banco de dados
- Painel para acompanhar importações
- Worker Python para automação por linha de comando

## Estrutura

```text
importador_excel_inteligente/
├── app.py
├── models.py
├── requirements.txt
├── .env.example
├── services/
│   ├── excel_service.py
│   ├── logger_config.py
│   └── validators.py
├── worker/
│   └── importar_excel_worker.py
├── web/
│   ├── index.html
│   └── static/
│       ├── app.js
│       └── estilos.css
├── arquivos_exemplo/
│   └── clientes_exemplo.xlsx
└── logs/
```

## Colunas obrigatórias do Excel

A planilha deve conter exatamente estas colunas:

- `nome`
- `documento`
- `email`
- `telefone`

## Como rodar

### 1) Criar ambiente virtual

```bash
python -m venv .venv
```

### 2) Ativar ambiente virtual

No PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

### 3) Instalar dependências

```bash
pip install -r requirements.txt
```

### 4) Rodar a API

```bash
python app.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

## Como usar o worker

Com a API rodando, execute:

```bash
python worker/importar_excel_worker.py arquivos_exemplo/clientes_exemplo.xlsx
```

## Regras de validação

- Nome precisa ter pelo menos 3 caracteres
- Documento precisa ter 11 ou 14 dígitos
- E-mail pode ser vazio, mas se vier preenchido precisa ter formato válido
- Telefone pode ser vazio, mas se vier preenchido precisa ter entre 10 e 13 dígitos

## Ideias para evolução

- autenticação JWT
- paginação das importações
- exportar erros para Excel
- dashboard com gráficos
- envio dos dados para API externa
