import pandas as pd
import pyodbc 
import json
import os

def get_connection(server: str, database: str, username: str, password: str):
    """Cria uma conexão com o banco de dados."""
    try:
        return pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
    except Exception as e:
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

def fetch_table_metadata(conn):
    """Obtém metadados das tabelas e colunas com extended properties."""
    query = """
        SELECT
            OBJECT_NAME(xp.major_id) AS tabela,
            col.name AS coluna,
            CONVERT(VARCHAR, xp.value) AS tag
        FROM
            sys.extended_properties xp
        JOIN
            sys.columns col
        ON  xp.major_id = col.object_id
        AND xp.minor_id = col.column_id
        WHERE
            col.name NOT LIKE '%_id%'
            AND col.name != 'id'
        ORDER BY 1;
    """
    return pd.read_sql(query, conn)

def fetch_sample_data(conn, tabela, coluna):
    query = f"SELECT TOP 1 CONVERT(VARCHAR, {coluna}) FROM dbo.{tabela}"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"Erro ao buscar exemplo para {tabela}.{coluna}: {e}")
        return None

def analyze_columns(df, categorias):
    """Classifica colunas com base em palavras-chave fornecidas."""
    resultados = []
    for categoria, itens in categorias.items():
        for idx, campo in enumerate(df["coluna"]):
            tabela = df["tabela"].iloc[idx]
            exemplo = df["exemplo_dado"].iloc[idx]
            for item in itens:
                if item.lower() in str(campo).lower():
                    resultados.append({
                        "coluna": campo,
                        "tabela": tabela,
                        "categoria": categoria,
                        "item_detectado": item,
                        "exemplo_dado": exemplo
                    })
    return pd.DataFrame(resultados)

def main():
    # Solicitar credenciais do usuário
    server = input("Digite o endereço do servidor: ")
    database = input("Digite o nome do database: ")
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Palavras-chave para classificação

    # Caminho para o arquivo JSON

    categorias_file = os.path.join(script_dir, 'categorias_tag.json')

    try:
        with open(categorias_file, 'r', encoding='utf-8') as file:
            categorias = json.load(file)
        print("Categorias carregadas com sucesso!")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{categorias_file}' não encontrado.")
        exit(1)

    # Conectar ao banco de dados
    conn = get_connection(server, database, username, password)

    # Buscar metadados
    df = fetch_table_metadata(conn)

    # Buscar exemplos de dados
    df_aux = pd.DataFrame(columns=["tabela", "coluna", "exemplo"])
    for index, row in df.iterrows():
        exemplo = fetch_sample_data(conn, row["tabela"], row["coluna"])
        df_aux = pd.concat(
            [df_aux, pd.DataFrame([{"tabela": row["tabela"], "coluna": row["coluna"], "exemplo": exemplo}])],
            ignore_index=True
        )

    df['exemplo_dado'] = df_aux["exemplo"]

    # Analisar colunas
    df_result = analyze_columns(df, categorias)

    # Salvar resultados
    
    output_file = os.path.join(script_dir, 'resultado_analise.csv')
    df_result.to_csv(output_file, index=False)
    
    # df_result.to_csv('resultado_analise.csv', index=False)
    print(f"Análise concluída e salva em '{output_file}'.")

    conn.close()

if __name__ == "__main__":
    main()
