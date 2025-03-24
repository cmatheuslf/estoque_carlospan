import psycopg2
import os
from dotenv import load_dotenv
from flask_login import UserMixin

#class user
class User(UserMixin):
        def __init__(self, id, login, email):
            self.id = id
            self.login = login
            self.email = email

        def get_id(self):
            return self.id

# Carrega variáveis de ambiente do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_connection():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def create_tables():
    """Cria as tabelas do banco de dados se não existirem."""
    conn = create_connection()
    if not conn:
        return
    
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS produto (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) UNIQUE NOT NULL,
                unidade VARCHAR(20) NOT NULL,
                preco NUMERIC(10,2) NOT NULL,
                estoque INTEGER DEFAULT 0
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) UNIQUE NOT NULL
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fluxo (
                id SERIAL PRIMARY KEY,
                produto_id INTEGER NOT NULL REFERENCES produtos(id),
                cliente_id INTEGER REFERENCES clientes(id),
                quantidade INTEGER NOT NULL,
                tipo VARCHAR(10) NOT NULL,  -- "entrada" ou "saída"
                valor_total NUMERIC(10,2) NOT NULL,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        print("Tabelas criadas com sucesso!")

    conn.close()
