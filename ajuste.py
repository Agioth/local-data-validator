import psycopg2

# Suas configurações de conexão
params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1234" # <-- Coloque sua senha real aqui
}

def executar_ajuste():
    conn = None
    try:
        # 1. Conecta ao banco
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        # 2. Define o comando SQL (agora como uma String Python)
        comando_sql = "ALTER TABLE auditoria_seo ADD CONSTRAINT unique_nome_empresa UNIQUE (nome_empresa);"
        
        print("Executando ajuste no banco de dados...")
        
        # 3. Envia o comando para o banco
        cur.execute(comando_sql)
        
        # 4. Salva a alteração
        conn.commit()
        
        print("Sucesso! A regra de Nome Único foi adicionada.")
        
        cur.close()
    except Exception as e:
        # Se der erro (ex: a regra já existe), ele avisa aqui
        print(f"Aviso/Erro: {e}")
    finally:
        # Garante que a conexão feche, dando certo ou errado
        if conn:
            conn.close()

if __name__ == "__main__":
    executar_ajuste()