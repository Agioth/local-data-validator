import psycopg2
from decimal import Decimal

# Configurações de conexão (Lembre de colocar sua senha)
params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1234"
}

def calcular_e_salvar_scores():
    try:
        # 1. Conecta ao banco de dados
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # 2. Busca os dados das empresas para analisar
        print("--- Lendo dados do PostgreSQL ---")
        cur.execute("SELECT id, nome_empresa, nota_google, reivindicado, telefone FROM auditoria_seo")
        empresas = cur.fetchall()

        if not empresas:
            print("Nenhum dado encontrado na tabela. Rode o coletor primeiro!")
            return

        print(f"Iniciando análise de {len(empresas)} registros...\n")

        for emp in empresas:
            emp_id, nome, nota, reivindicado, telefone = emp
            
            # --- O ALGORITMO DE SCORE (Começa com 100 pontos) ---
            score = 100

            # Penalidade 1: Falta de Telefone (-40 pontos)
            # É o pior problema para um negócio local
            if telefone == "Não encontrado" or not telefone:
                score -= 40
            
            # Penalidade 2: Perfil sem dono/não reivindicado (-30 pontos)
            if not reivindicado:
                score -= 30

            # Penalidade 3: Nota baixa ou inexistente (-20 a -25 pontos)
            if nota and float(nota) < 4.2:
                score -= 20
            elif not nota:
                score -= 25

            # --- DEFININDO O NÍVEL DE PRIORIDADE ---
            if score <= 40:
                nivel = "CRÍTICA"
            elif score <= 70:
                nivel = "MÉDIA"
            else:
                nivel = "BAIXA"

            # --- GRAVANDO O RESULTADO NO BANCO DE DADOS ---
            cur.execute("""
                UPDATE auditoria_seo 
                SET score_prioridade = %s, nivel_prioridade = %s 
                WHERE id = %s
            """, (score, nivel, emp_id))
            
            print(f"✅ Analisado: {nome[:25]}... | Score: {score} | Status: {nivel}")

        # Salva as alterações permanentemente
        conn.commit()
        print("\n--- ANALISE CONCLUÍDA E SALVA COM SUCESSO ---")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erro durante a análise: {e}")

if __name__ == "__main__":
    calcular_e_salvar_scores()