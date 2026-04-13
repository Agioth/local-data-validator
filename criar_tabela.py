import psycopg2
from database import get_connection # ADICIONE NO TOPO

conn = get_connection() # USE ASSIM

def criar_estrutura():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS auditoria_seo (
            id SERIAL PRIMARY KEY,
            nome_empresa VARCHAR(255) NOT NULL,
            categoria VARCHAR(100),
            nota_google DECIMAL(2,1),
            reivindicado BOOLEAN DEFAULT FALSE,
            comentarios_nao_respondidos INTEGER DEFAULT 0,
            ultima_postagem_dias INTEGER,
            tem_site BOOLEAN DEFAULT FALSE,
            score_saude INTEGER,
            data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )
    
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Executa o comando de criação
        for command in commands:
            cur.execute(command)
            
        cur.close()
        conn.commit()
        print("-" * 30)
        print("TABELA 'auditoria_seo' CRIADA COM SUCESSO!")
        print("-" * 30)
        
    except Exception as e:
        print(f"ERRO AO CRIAR TABELA: {e}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    criar_estrutura()