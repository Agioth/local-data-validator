import os
import psycopg2
import logging
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Configuração do Log (Cria o rastro profissional)
# Configuração do Log Blindado e com acentos corretos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # Adicionamos o encoding="utf-8" aqui:
        logging.FileHandler("app_robusto.log", encoding="utf-8"), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_connection():
    """Retorna uma conexão com o banco de dados com tratamento de erros."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )
        logger.info("Conexão com o Banco de Dados estabelecida com sucesso.")
        return conn
    except Exception as e:
        # Se a senha estiver errada ou o banco estiver offline, ele cai aqui:
        logger.error(f"ERRO CRÍTICO ao conectar no banco: {e}")
        return None