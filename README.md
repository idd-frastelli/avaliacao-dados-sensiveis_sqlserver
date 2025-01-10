# Avaliação de Dados Sensíveis

Este projeto tem como objetivo identificar possíveis dados sensíveis armazenados em bancos de dados, com base na nomenclatura das colunas.

## Estrutura do Repositório
```
avaliacao-dados-sensiveis_sqlserver/ 
├── src/ 
│ ├── main.py 
│ ├── utils.py 
│ ├── categorias_tag.json 
├── .gitignore 
├── README.md 
├── requirements.txt 
└── LICENSE 
```

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/avaliacao-dados-sensiveis_sqlserver.git
   cd avaliacao-dados-sensiveis_sqlserver

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

1. Execute o script principal:
```bash
   python src/main.py
```

3. Insira as credenciais e informações do banco de dados: server (IP), database, username e password

4. O arquivo final, resultado_analise.csv, conterá todos os campos que foram identificados conforme documentação.

