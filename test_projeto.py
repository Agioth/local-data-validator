import os
from database import get_connection
from models import CompanyModel
from dotenv import load_dotenv

def testar_sistema():
    print("🚀 Iniciando Teste de Robustez do Smart Cat Pro...\n")

    # 1. Teste de Ambiente (.env)
    print("1. Verificando Variáveis de Ambiente...")
    load_dotenv()
    if os.getenv("DB_PASS"):
        print("✅ Arquivo .env carregado com sucesso!")
    else:
        print("❌ ERRO: Arquivo .env não encontrado ou vazio!")
        return

    # 2. Teste de Conexão com o Banco
    print("\n2. Testando Conexão com PostgreSQL...")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"✅ Conectado ao Banco! Versão: {db_version[0][:25]}...")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ ERRO de Conexão: {e}")
        return

    # 3. Teste de Lógica do Pydantic (O "Coração" do projeto)
    print("\n3. Validando Lógica de Scoring (Pydantic)...")
    try:
        dados_teste = {
            "name": "Loja Teste",
            "phone": "(91) 98888-7777", # Telefone com 9 dígitos
            "rating": 4.5,
            "is_claimed": True
        }
        # Se o seu model pede fotos ou outros campos, o Pydantic vai validar aqui
        lead = CompanyModel(**dados_teste)
        
        score = lead.leads_quality_score
        print(f"✅ Model funcionando! Telefone limpo: {lead.phone}")
        print(f"✅ Score calculado: {score}")
        
        if score == 100:
            print("🔥 Teste de Lógica: Lead Perfeito identificado.")
        else:
            print("⚠️ Teste de Lógica: Lead com melhorias identificado.")
            
    except Exception as e:
        print(f"❌ ERRO no Model: {e}")
        return

    print("\n" + "="*30)
    print("✨ TUDO OK! Projeto pronto para o GitHub.")
    print("="*30)

if __name__ == "__main__":
    testar_sistema()