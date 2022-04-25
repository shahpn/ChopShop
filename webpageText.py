from flask import Flask
from flask import render_template
from PIL import Image


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

#



