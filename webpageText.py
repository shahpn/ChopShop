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
#     #Gabe yada yada 'to-do comments. Don't mind me ty
    #TODO 1 - Setup image on the right side, lined up with the "Enter your grocery list in the section below:" (Image not loading)
    #TODO 2 - Take text area input and split each line as separate element in list
    #TODO 3 - Create a top view of our store. Realistic visual, not graph visual
    #TODO 4 - Use Pillow library to draw the path from E to CO (Will find a pretier solution later)
    #TODO 5 - Add labels that are OVER the image to label what item is at each destination


