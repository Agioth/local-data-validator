import psycopg2
import sys

# Parâmetros de conexão
params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1234" # <--- Troque pela sua senha
}

try:
    print("Iniciando tentativa de conexão...")
    conn = psycopg2.connect(**params)
    
    print("-" * 30)
    print("SISTEMA ONLINE - CONEXÃO BEM SUCEDIDA")
    print("-" * 30)

    conn.close()

except Exception as e:
    # Captura o erro bruto e limpa caracteres não-ascii para evitar o crash de UTF-8
    error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
    print(f"\n[ERRO DE ENGENHARIA]: {error_msg}")
    print("\nVerifique se a SENHA está correta ou se o USUÁRIO existe.")