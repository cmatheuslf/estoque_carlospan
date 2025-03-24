from flask import Flask, request, Blueprint, jsonify, request, redirect, url_for, render_template
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
from flask_login import LoginManager,  login_user, login_required, current_user
import hashlib
from models import User
from routes.pages import pages


# Carrega variáveis do .env
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

def create_app():
    """Inicializa o Flask app."""
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")  # Necessário para sessões Flask-Login
    CORS(app)

    # Teste de conexão com o banco
    conn = create_connection()
    if conn:
        print("Banco de dados conectado com sucesso!")
        conn.close()

    # Importação e registro de rotas
    from routes.produtos.produtos_bp import produtos_bp
    from routes.clientes.clientes_bp import clientes_bp
    from routes.fluxos.fluxos_bp import fluxos_bp
    #from routes.usuarios.usuarios_bp import usuarios_bp

    app.register_blueprint(produtos_bp, url_prefix='/produtos')
    # app.register_blueprint(clientes_bp, url_prefix='/clientes')
    # app.register_blueprint(fluxos_bp, url_prefix='/fluxos')
    #app.register_blueprint(usuarios_bp, url_prefix='/user')

    
    lm = LoginManager(app)

    

    def get_db_connection():
        """Cria uma conexão com o banco de dados PostgreSQL."""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            return conn
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def hash_generator(txt):
        """Gera um hash SHA-256 combinando login e email."""
        hash_obj = hashlib.sha256(txt.encode())  # Converte para SHA-256
        return hash_obj.hexdigest()  # Retorna o hash em hexadecimal

    @lm.user_loader
    def user_loader(id):
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
        user = ""
        with conn.cursor() as cur:
            cur.execute("Select login, email from usuario  where id = %s", (id,))
            user = cur.fetchone()
        email =""
        login= ""
        if not user:
            return None

        #login, email = user
        user = User(id, login, email)
        login_user(user)

        return user     
    
    @app.route('/', methods=['GET'])
    def home():
        page = pages.home()

        return page

    @app.route('/register', methods=['POST'])
    def register():

        data = request.get_json()  # Obtém os data enviados no corpo da requisição

        if not data:
            return jsonify({"error": "JSON inválido ou não enviado"}), 400

        login = data.get("login")
        password = data.get("password")
        email = data.get("email")
        id = hash(login)

        if not login or not password:
            return jsonify({"error": "Campos 'login' e 'password' são obrigatórios"}), 400
        """Lista todos os usuarios."""
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
        
        
        with conn.cursor() as cur:
            cur.execute("INSERT INTO usuario (id,login, password, email) VALUES (%s, %s, %s, %s)",
                    (id, login, password, email))
            conn.commit()  # colocando no bd
        
        conn.close()
        user = User(login, password, email)
        login_user(user)
        return jsonify(200)
    
    @app.route('/login', methods=['GET'])
    def login_page():
        page = pages.login()

        return page
        
    
        
    
    @app.route('/login_data', methods=['POST'])
    def login():

        data = request.get_json()  # Obtém os data enviados no corpo da requisição

        if not data:
            return jsonify({"error": "JSON inválido ou não enviado"}), 400

        login = data.get("login")
        password = data.get("password")

        if not login or not password:
            return jsonify({"error": "Campos 'login' e 'password' são obrigatórios"}), 400
        """Lista todos os usuarios."""
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
        
        user = ""
        with conn.cursor() as cur:
            cur.execute('Select id, login, email From usuario Where login = %s and "password" = %s', (login, password))
            conn.commit()  # colocando no bd
            user = cur.fetchone()
        
        conn.close()
        id =""
        email =""
        login= ""
        print(user)
        id, login, email = user
        user = User(id, login, email)
        login_user(user)
        return jsonify(200)

    return app
