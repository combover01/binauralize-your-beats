from flask import render_template, Flask
app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/edu")
def edu():
    return render_template("edu.html")
