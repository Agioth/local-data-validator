import psycopg2
import csv

params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1234"
}

def exportar_final():
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Pegamos os dados limpinhos do banco
        cur.execute("""
            SELECT nome_empresa, telefone, data_analise 
            FROM auditoria_seo 
            WHERE telefone != 'Não encontrado'
            ORDER BY nome_empresa ASC;
        """)
        
        dados = cur.fetchall()
        arquivo = "leads_castanhal_limpo.csv"

        with open(arquivo, mode='w', newline='', encoding='utf-8-sig') as f:
            escritor = csv.writer(f, delimiter=';')
            escritor.writerow(['Empresa', 'Telefone', 'Data da Coleta'])
            escritor.writerows(dados)

        print(f"✅ RELATÓRIO GERADO: {arquivo}")
        print(f"Foram exportados {len(dados)} contatos limpos.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    exportar_final()