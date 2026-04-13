import psycopg2

params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1234" 
}

def atualizar_banco():
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print("Conectado! Iniciando migracao...")
        
        # Criando as colunas se nao existirem
        cur.execute("ALTER TABLE auditoria_seo ADD COLUMN IF NOT EXISTS telefone VARCHAR(30);")
        cur.execute("ALTER TABLE auditoria_seo ADD COLUMN IF NOT EXISTS nota_google DECIMAL(2,1);")
        
        # Criando a regra de nome unico
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'unique_nome_empresa') THEN
                    ALTER TABLE auditoria_seo ADD CONSTRAINT unique_nome_empresa UNIQUE (nome_empresa);
                END IF;
            END $$;
        """)
        
        conn.commit()
        print("BANCO ATUALIZADO COM SUCESSO!")
        
    except Exception as e:
        print(f"Erro na migracao: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    atualizar_banco()