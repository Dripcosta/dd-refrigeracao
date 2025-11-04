from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__, template_folder='templates')

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Cria tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    # Cria tabela de agendamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            servico TEXT NOT NULL
        )
    ''')

    # Cria usuário padrão
    cursor.execute("INSERT OR IGNORE INTO usuarios (id, usuario, senha) VALUES (1, 'admin', '1234')")

    conn.commit()
    conn.close()

init_db()

# Página principal
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agendamentos")
    agendamentos = cursor.fetchall()
    conn.close()
    return render_template('index.html', agendamentos=agendamentos)

# Login do administrador
@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    user = cursor.fetchone()
    conn.close()
    if user:
        return redirect('/')
    else:
        return "Login inválido"

# Agendamento de serviço
@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome']
    data = request.form['data']
    servico = request.form['servico']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agendamentos (nome, data, servico) VALUES (?, ?, ?)", (nome, data, servico))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
