from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro/', methods=["GET", "POST"])
def login():
    return render_template('cadastro.html')


if __name__ == '__main__':
    app.run(debug=True)