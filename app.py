from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "clee"

@app.route('/')
def hello_method():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    _from = request.form['from']
    _to = request.form['to']
    path = "../static/test_pic.png"
    return render_template("map.html", data=path)

if __name__ == '__main__':
    app.run()