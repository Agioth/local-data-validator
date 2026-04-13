import psycopg2
import csv
from models import CompanyModel
from database import get_connection # ADICIONE NO TOPO

conn = get_connection() # USE ASSIM

def exportar_final():
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT nome_empresa, categoria, telefone, nota_google, reivindicado, comentarios_nao_respondidos 
                    FROM auditoria_seo 
                    WHERE telefone != 'Não encontrado'
                    ORDER BY nome_empresa ASC;
                """)
                
                dados_brutos = cur.fetchall()
                arquivo = "leads_castanhal_premium.csv"

                with open(arquivo, mode='w', newline='', encoding='utf-8-sig') as f:
                    escritor = csv.writer(f, delimiter=';')
                    
                    # --- LEGENDA DO RELATÓRIO (Aparecerá no topo do Excel) ---
                    escritor.writerow(['LEGENDA DE CLASSIFICAÇÃO'])
                    escritor.writerow(['STATUS', 'CRITÉRIO', 'DESCRIÇÃO'])
                    escritor.writerow(['🔥 Ouro', 'Score <= 30', 'Alta urgência: Erros graves de SEO/Presença Digital.'])
                    escritor.writerow(['👀 Oportunidade', 'Score > 30', 'Médio prazo: Possui presença básica, mas precisa de ajustes.'])
                    escritor.writerow([]) # Linha em branco para separar da tabela
                    
                    # Cabeçalho da tabela de dados
                    escritor.writerow(['Empresa', 'Telefone Limpo', 'Score', 'Status'])

                    for linha in dados_brutos:
                        lead = CompanyModel(
                            name=linha[0],
                            phone=linha[2],
                            rating=linha[3] if linha[3] else 0.0,
                            is_claimed=linha[4] if linha[4] is not None else False
                        )
                        
                        score_final = lead.leads_quality_score
                        
                        if score_final <= 30:
                            status = "🔥 Ouro"
                        else:
                            status = "👀 Oportunidade"
                        
                        escritor.writerow([lead.name, lead.phone, score_final, status])

                print("-" * 40)
                print(f"✅ SUCESSO: {arquivo} gerado com legenda!")
                print(f"📊 {len(dados_brutos)} leads exportados.")
                print("-" * 40)

    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")

if __name__ == "__main__":
    exportar_final()