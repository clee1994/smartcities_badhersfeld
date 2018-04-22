from flask import Flask, render_template, request

from route_bhf import create_route, string_to_xy

app = Flask(__name__)
app.secret_key = "clee"

@app.route('/')
def hello_method():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    _from = request.form['from']
    _to = request.form['to']

    from_xy = string_to_xy(_from)
    to_xy = string_to_xy(_to)

    path = create_route(from_xy,to_xy)
    #path = "../static/test_pic.png"
    return render_template("map.html", data=path)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')