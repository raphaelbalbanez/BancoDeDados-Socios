from flask import Flask, render_template, request, url_for, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__,template_folder='Templates')



conexao = {
    'port':3306,
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'SocioClube',
}


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('cadastrar_socios.html')


@app.route('/cadastrar_socios', methods=['GET','POST'])
def cadastrar_socio():
    if request.method == 'POST':
        socios = request.form.get('nome')    
        cpf = request.form.get('cpf')
        data_nasc = request.form.get('d_nasc')

        dados = mysql.connector.connect(**conexao)
        cursor = dados.cursor()
        banco = 'INSERT INTO socioclube.socios(nome, cpf, d_nasc)VALUES(%s,%s,%s);'
        try:
            cursor.execute(banco, valor_socio)
            dados.commit()
            print("INSERIDOOOOOOOOOOOO")
        except Exception as e:
            print(f"Erro ao inserir no banco de dados: {e}")

        valor_socio = (socios, cpf, data_nasc)
        cursor.execute(banco,valor_socio)
        dados.commit()
        
    return render_template('cadastrar_socios.html')


@app.route('/mostrar_socios', methods=['GET'])
def mostrar_socio():
    if request.method == 'GET':
        filter_age = request.args.get('filter_age')

        dados = mysql.connector.connect(**conexao)
        cursor = dados.cursor()

        if filter_age:
            # Modifique a consulta para incluir a condição de filtro
            banco = 'SELECT * FROM socioclube.socios WHERE TIMESTAMPDIFF(YEAR, d_nasc, CURDATE()) <= %s;'
            cursor.execute(banco, (filter_age,))
        else:
            banco = 'SELECT * FROM socioclube.socios;'
            cursor.execute(banco)

        socios = cursor.fetchall()
        cursor.close()
        dados.close()

    return render_template('mostrar_socios.html', socios=socios)

    

@app.route('/deletar_socio/<string:cpf>', methods=['POST'])
def deletar_socio(cpf):
    dados = mysql.connector.connect(**conexao)
    cursor = dados.cursor()
    banco = 'DELETE FROM socioclube.socios WHERE cpf = %s;'
    cursor.execute(banco, (cpf,))
    dados.commit()
    cursor.close()
    dados.close()

    return redirect(url_for('mostrar_socio'))


@app.route('/editar_socio/<cpf>', methods=['GET', 'POST'])
def editar_socio(cpf):
    conn = mysql.connector.connect(**conexao)
    cursor = conn.cursor()

    cursor.execute("SELECT nome, cpf, d_nasc FROM socios WHERE cpf = %s", (cpf,))
    socio = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        d_nasc = request.form['d_nasc']

        cursor.execute("UPDATE socios SET nome=%s, d_nasc=%s WHERE cpf=%s", (nome, d_nasc, cpf))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('mostrar_socio'))

    cursor.close()
    conn.close()
    return render_template('editar_socio.html', socio=socio)

@app.route('/consulta_socios', methods=['GET', 'POST'])
def consulta_socios():
    if request.method == 'POST':
        nome_pesquisado = request.form.get('nome_pesquisado')

        dados = mysql.connector.connect(**conexao)
        cursor = dados.cursor()

        # Consulta normal
        if 'consulta_mais_velho' not in request.form and 'consulta_mais_novo' not in request.form:
            banco = 'SELECT * FROM socioclube.socios WHERE nome = %s;'
            cursor.execute(banco, (nome_pesquisado,))
            socio = cursor.fetchone()

        # Consulta do sócio mais velho
        elif 'consulta_mais_velho' in request.form:
            banco = 'SELECT * FROM socioclube.socios WHERE d_nasc = (SELECT MIN(d_nasc) FROM socioclube.socios);'
            cursor.execute(banco)
            socio = cursor.fetchone()

        # Consulta do sócio mais novo
        elif 'consulta_mais_novo' in request.form:
            banco = 'SELECT * FROM socioclube.socios WHERE d_nasc = (SELECT MAX(d_nasc) FROM socioclube.socios);'
            cursor.execute(banco)
            socio = cursor.fetchone()

        cursor.close()
        dados.close()

        if socio:
            return render_template('consulta_socios.html', socio=socio)
        else:
            mensagem = "Nenhum sócio cadastrado com esse nome."
            return render_template('consulta_socios.html', mensagem=mensagem)

    return render_template('consulta_socios.html')


    
if __name__ == '__main__':
    app.run(debug=True)

