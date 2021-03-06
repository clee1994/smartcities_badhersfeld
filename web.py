from flask import Flask, render_template, json, request, redirect, url_for
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/map")
def showMap():
    return render_template('map.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    _from = request.form['inputName']
    _to = request.form['inputEmail']
    return render_template('map.html')

if __name__ == "__main__":
    app.run()