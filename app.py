from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import smtplib, hashlib
import sqlite3

app = Flask(__name__,template_folder='view', static_folder='view', static_url_path='')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/", methods=['GET', 'POST'])
def Index():    
    if 'Logado' in session:
        return render_template('menu.html', user = session['user'])
    else:
        return render_template('index.html')
    
    return render_template('index.html')

@app.route("/usuario", methods=['GET', 'POST'])
def usuario():
    if request.method == 'POST':
        dados = request.get_json()
        user = dados[0]['user']
        passw = dados[1]['passw']
        banco = sqlite3.connect('user.db')
        cursor = banco.cursor()
        
        sql = "SELECT * FROM user WHERE usuario = '{}' and senha = '{}'".format(user, passw)

        cursor.execute(sql)
        banco.commit()
        resultadoBanco = cursor.fetchall()
        print(resultadoBanco)
        
        for login in resultadoBanco:
            if user == login[1] and passw == login[2]:
                session['Logado'] = True
                session['user'] = user
                return redirect(url_for("logado"))
        else:
            results = {'processed': 'false'}
            print('Entrou no 1')
            return jsonify(results)
    return render_template('index.html')

@app.route("/logado")
def logado():
    if 'Logado' in session:
        results = {'processed': 'true'}
        print('Entrou no 2')
        return jsonify(results)
    return render_template('index.html')               

if __name__ == '__main__':
    app.run(port=8080, debug=True)