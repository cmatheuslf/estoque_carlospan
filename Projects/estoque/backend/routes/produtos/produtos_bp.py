from flask import Flask, request, Blueprint, jsonify, request, redirect, url_for, render_template
from flask_login import LoginManager,  login_user, login_required, current_user
import psycopg2
import os
from dotenv import load_dotenv
from ..pages import pages

# Carrega variáveis do .env jsonify(produtos_lista)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

produtos_bp = Blueprint('produtos', __name__, template_folder="../../templates/product")
######################3 PAGES ###########################

@produtos_bp.route('/', methods=['GET'])
@login_required
def list_products():
    return render_template('lista.html')

#renderizando pagina
@produtos_bp.route('/insert_page', methods=['GET'])
@login_required
def page_insert_products():
    return render_template('inserir_produtos.html')

@produtos_bp.route('/edit', methods=['GET'])
@login_required
def page_update_products():
    return render_template('edit_products.html')


##########################################################
def get_db_connection():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None



@produtos_bp.route('/list_products', methods=['GET'])
@login_required
def listar_produtos():
    """Lista todos os produtos."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM produto")
        produtos = cur.fetchall()
    
    conn.close()
    
    produtos_lista = [
        {
                    "pnome": produto[0],
                    "cbarra": produto[1],
                    "medida": produto[2],
                    "quantidade": produto[3],
                    "alerta": produto[4]
                }
                  for produto in produtos]
    return jsonify(produtos_lista) 

@produtos_bp.route('/new', methods=['POST'])
@login_required
def create_product():
    data = request.get_json()

    pnome = data.get("pnome")
    cbarra = data.get("cbarra")
    medida = data.get("medida")
    quantidade = data.get("quantidade")
    alerta = data.get("alerta")

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO produto (pnome, cbarra, medida, quantidade, alerta) VALUES(%s,%s,%s,%s,%s)", (pnome, cbarra, medida, quantidade, alerta))
            conn.commit()
    except Exception as e:
        return jsonify("Algo deu errado contate o time de suporte: 85 98417-4059")

    return jsonify("sucesso ao criar novo produto")

@produtos_bp.route('/read', methods=['GET'])
@login_required
def read_product():
    data = request.get_json()

    cbarra = data.get("cbarra")

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT pnome , cbarra , medida , quantidade , alerta FROM produto WHERE cbarra = %s", (cbarra,))
            produto = cur.fetchone()
            if id:
                produto_json = {
                    "pnome": produto[0],
                    "cbarra": produto[1],
                    "medida": produto[2],
                    "quantidade": produto[3],
                    "alerta": produto[4]
                }
                return jsonify(produto_json), 200
            else:
                return jsonify("Produto não encontrado, verifique o código de barras digitado.")
    except Exception as e:
        return jsonify("Algo deu errado contate o time de suporte: 85 98417-4059", str(e))

@produtos_bp.route('/update', methods=['POST'])
@login_required
def update_product():
    data = request.get_json()

    pnome = data.get("pnome")
    cbarra = data.get("cbarra")
    medida = data.get("medida")
    quantidade = data.get("quantidade")
    alerta = data.get("alerta")
    id = 0

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE produto SET pnome = %s, cbarra = %s, medida = %s, quantidade = %s, alerta = %s WHERE cbarra = %s RETURNING cbarra;", (pnome, cbarra, medida, quantidade, alerta, cbarra))
            id = cur.fetchone()
            if id:
                conn.commit()
                return jsonify("sucesso ao criar atualizar produto")
            else:
                return jsonify("Produto não encontrado, verifique o código de barras digitado.")
    except Exception as e:
        return jsonify("Algo deu errado contate o time de suporte: 85 98417-4059", str(e))

@produtos_bp.route('/delete', methods=['POST'])
@login_required
def delete_product():
    data = request.get_json()

    cbarra = data.get("cbarra")

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM produto WHERE cbarra = %s", (cbarra,))
            conn.commit()
    except Exception as e:
        return jsonify("Algo deu errado contate o time de suporte: 85 98417-4059")

    return jsonify("sucesso ao deletar produto")
