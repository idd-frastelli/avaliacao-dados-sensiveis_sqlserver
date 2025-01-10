# Avaliação de Dados Sensíveis

Este projeto tem como objetivo identificar possíveis dados sensíveis armazenados em bancos de dados, com base na nomenclatura das colunas.

## Estrutura do Repositório
avaliacao-dados-sensiveis/ ├── src/ │ ├── main.py │ ├── utils.py │ ├── categorias_tag.json ├── tests/ │ ├── test_utils.py │ ├── test_main.py ├── .gitignore ├── README.md ├── requirements.txt └── LICENSE

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/avaliacao-dados-sensiveis.git
   cd avaliacao-dados-sensiveis

2. Instale as dependências:
pip install -r requirements.txt

## Execução

1. Execute o script principal:  python src/main.py

2. Insira as credenciais e informações do banco de dados: server (IP), database, username e password

