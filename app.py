from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('searchBarSample.html')


if __name__ == '__main__':
    app.run(debug=True, port=5002)
