import sqlite3
from flask import Flask, request, session, g, redirect, abort, render_template, flash, url_for

#Configuração
DATABASE = "blog.db"
SECRET_KEY = 'pudim'

app = Flask(__name__)
app.config.from_object(__name__)

#Funções de acesso ao banco de dados(obs: @app é o decorator)
def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def antes_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def depois_request(exc):
    g.bd.close()


#Funções de rota
@app.route('/')
@app.route('/entradas')
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    for titulo, texto in cur.fetchall():
        entradas.append({'titulo': titulo, 'texto': texto})
    return render_template('exibir_entradas.html', entradas=entradas)

@app.route('/inserir')
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql =  "INSERT INTO entradas (titulo, texto) VALUES (?,?)"
    g.bd.execute(sql,request.form['campoTitulo'] , request.form['campoTexto'] )
    g.bd.commit()
    return redirect(url_for('exibir_entradas'))
