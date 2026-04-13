import psycopg2

params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1234"
}

def consultar_relatorio():
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Agora pedimos para o banco trazer o telefone também!
        cur.execute("SELECT id, nome_empresa, telefone, data_analise FROM auditoria_seo;")
        linhas = cur.fetchall()

        print("-" * 80)
        print(f"{'ID':<4} | {'NOME DA EMPRESA':<35} | {'TELEFONE':<15} | {'DATA'}")
        print("-" * 80)

        for l in linhas:
            # l[2] agora é o telefone
            tel = l[2] if l[2] else "---"
            print(f"{l[0]:<4} | {l[1]:<35} | {tel:<15} | {l[3].strftime('%d/%m %H:%M')}")

        print("-" * 80)
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    consultar_relatorio()