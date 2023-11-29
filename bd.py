from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Rapha Barros", "LUX", "euvouparaalux")
usuario2 = Usuario("Renato Santana", "Nagas", "renagol87")
usuario3 = Usuario("Joao Augusto", "Burgo", "dogsburgo")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

app = Flask(__name__)
app.secret_key = 'bd'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)