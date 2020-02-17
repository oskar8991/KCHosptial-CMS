from flask import Flask
from flask import Flask, url_for, redirect, render_template, request, session, abort, flash

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin':
            flash('Invalid credentials')
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('auth/login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()



if __name__ == '__main__':
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()

