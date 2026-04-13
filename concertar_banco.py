import psycopg2

params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "SUA_SENHA_AQUI"
}

def consertar():
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        print("Adicionando colunas e regras de segurança...")
        
        # 1. Adiciona a coluna de telefone que estava faltando
        cur.execute("ALTER TABLE auditoria_seo ADD COLUMN IF NOT EXISTS telefone VARCHAR(20);")
        
        # 2. Adiciona a coluna de nota e site (já para adiantar o próximo passo)
        cur.execute("ALTER TABLE auditoria_seo ADD COLUMN IF NOT EXISTS nota_google DECIMAL(2,1);")
        cur.execute("ALTER TABLE auditoria_seo ADD COLUMN IF NOT EXISTS tem_site BOOLEAN DEFAULT FALSE;")
        
        # 3. Cria a regra de que o nome da empresa deve ser único (para o ON CONFLICT funcionar)
        cur.execute("ALTER TABLE auditoria_seo ADD CONSTRAINT unique_nome_empresa UNIQUE (nome_empresa);")
        
        conn.commit()
        print("BANCO ATUALIZADO COM SUCESSO! Agora as gavetas estão prontas.")
        
    except Exception as e:
        print(f"Aviso/Erro: {e} (Se disser que a regra já existe, ignore, é bom sinal!)")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    consertar()