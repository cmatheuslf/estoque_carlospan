from flask import Blueprint, jsonify
import psycopg2
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

clientes_bp = Blueprint('clientes', __name__)

def get_db_connection():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@clientes_bp.route('/', methods=['GET'])
def listar_clientes():
    """Lista todos os clientes."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    with conn.cursor() as cur:
        cur.execute("SELECT id, nome, unidade, preco, estoque FROM clientes")
        clientes = cur.fetchall()
    
    conn.close()
    
    clientes_lista = [{"id": p[0], "nome": p[1], "unidade": p[2], "preco": float(p[3]), "estoque": p[4]} for p in clientes]
    return jsonify(clientes_lista)
