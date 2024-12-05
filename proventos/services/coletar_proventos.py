import sqlite3
from django.conf import settings
import os
from proventos.services.dividendos import Dividendo  # Updated import
def atualizar_proventos():
    database_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Criar tabela de proventos
    cursor.execute('''CREATE TABLE IF NOT EXISTS proventos
                     (papel TEXT, data_com DATE, data_pagamento DATE, 
                      tipo_provento TEXT, valor_provento REAL, 
                      por_quantas_acoes INTEGER)''')

    # Pegar lista de ativos do portfolio
    cursor.execute("SELECT DISTINCT Ativo FROM portfolio_consolidadas")
    ativos = [row[0] for row in cursor.fetchall()]

    # Coletar proventos para cada ativo
    for ativo in ativos:
        proventos = Dividendo(ativo).pegar_dividendos_acao()
        if not proventos.empty:
            proventos.to_sql('proventos', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
