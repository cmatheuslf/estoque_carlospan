from flask import Blueprint, jsonify, request, redirect
from flask_login import LoginManager,  login_user
import psycopg2
import os
from dotenv import load_dotenv
import hashlib



lm = LoginManager(app)
# Carrega variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

usuarios_bp = Blueprint('usuarios', __name__)
def id_generator(login, email):
    """Gera um hash SHA-256 combinando login e email."""
    texto = f"{login}{email}"  # Concatena os valores
    hash_obj = hashlib.sha256(texto.encode())  # Converte para SHA-256
    return hash_obj.hexdigest()  # Retorna o hash em hexadecimal

@lm.user_loader
def user_loader(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    user = ""
    with conn.cursor() as cur:
        cur.execute("Select login from usuario  where id == $s", id)
        user = cur.fetchone
    return user

def get_db_connection():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@usuarios_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()  # Obtém os data enviados no corpo da requisição

    if not data:
        return jsonify({"error": "JSON inválido ou não enviado"}), 400

    login = data.get("login")
    password = data.get("password")
    email = data.get("email")
    id = id_generator(login, email)

    if not login or not password:
        return jsonify({"error": "Campos 'login' e 'password' são obrigatórios"}), 400
    """Lista todos os usuarios."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    with conn.cursor() as cur:
        cur.execute("INSERT INTO usuario (id,login, password, email) VALUES (%s, %s, %s, %s)",
                (id, login, password, email))
    
    conn.close()
    login_user(login, password)
    return jsonify(200)
