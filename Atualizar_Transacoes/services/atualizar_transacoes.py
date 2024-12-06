from django.conf import settings
import os
import pandas as pd
import sqlite3
from datetime import datetime

def atualizar_transacoes():
    import os
    from pathlib import Path

    # Obtém o caminho do Desktop de forma dinâmica
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

    # Define os caminhos relativos ao Desktop
    origem_path1 = os.path.join(desktop, 'TRADERSPLAN-3.401 MONICA', 'TRADERS PLAN_3.45 PRO.xlsm')
    origem_path2 = os.path.join(desktop, 'TRADERSPLAN-3.401 SILMAR', 'TRADERS PLAN_3.45 PRO.xlsm')
    database_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    datas_atualizadas = set()

    def processar_planilha(path):
        df = pd.read_excel(path, sheet_name="OPERAÇÕES", usecols="A:G")
        df = df.iloc[1:]
        df.columns = ['Data', 'Operacao', 'Ativo', 'Quantidade', 'Preço', 'Nota', 'Corretora']
        df['Data'] = pd.to_datetime(df['Data']).dt.date
        return df

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Obter datas existentes antes da atualização
    datas_antigas = set()
    for tabela in ['transacoes_monica', 'transacoes_silmar']:
        cursor.execute(f"SELECT DISTINCT Data FROM {tabela}")
        datas_antigas.update(row[0] for row in cursor.fetchall())

    # Processar novas transações
    df_monica = processar_planilha(origem_path1)
    df_silmar = processar_planilha(origem_path2)

    # Limpar e inserir dados
    cursor.execute("DELETE FROM transacoes_monica")
    cursor.execute("DELETE FROM transacoes_silmar")
    cursor.execute("DELETE FROM transacoes_consolidadas")

    def inserir_dados(df, tabela):
        cursor.executemany(f"""
            INSERT INTO {tabela} (Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, df.values.tolist())
        return set(df['Data'].unique())

    # Inserir e coletar datas atualizadas
    datas_atualizadas.update(inserir_dados(df_monica, "transacoes_monica"))
    datas_atualizadas.update(inserir_dados(df_silmar, "transacoes_silmar"))

    # Consolidar dados
    cursor.execute("""
        INSERT INTO transacoes_consolidadas (Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora)
        SELECT Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora FROM transacoes_monica
        UNION ALL
        SELECT Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora FROM transacoes_silmar
    """)

    conn.commit()
    conn.close()

    # Retornar datas que precisam ser atualizadas (novas ou modificadas)
    datas_para_atualizar = datas_atualizadas - datas_antigas
    return sorted(list(datas_para_atualizar))

if __name__ == "__main__":
    atualizar_transacoes()