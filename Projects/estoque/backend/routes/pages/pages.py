from flask import Flask, request, Blueprint, jsonify, request, redirect, url_for, render_template
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
from flask_login import LoginManager,  login_user, login_required, current_user

   

def home():
    return render_template('home.html')

def login():
    return render_template('login.html')

def insert_products():
    return render_template('inserir_produtos.html')

def list_products():
    return render_template('lista.html')