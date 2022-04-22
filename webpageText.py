from flask import Flask
from PIL import Image


app = Flask(__name__)
@app.route("/")
def home():
    text ="<head>"\
    "<style>"\
    "h1 {text-align: center;}"\
    "h4 {text-align: center;}" \
    "p {text-align: left;}"\
    "div {text-align: center;}" \
    "</style>"\
    "</head>" \
    "<title> BluPrnt </title>" \
    "<p style = color:red >"\
    "<h1>Welcome To ChopShop<h1>" \
    "<h4> Presented to you by PythonPals &#128151 Industries <h4>" \
    "<body>" \
    "<body style=background-color:powderblue;>" \
    "<p> Enter your grocery list in the section below: <p>" \
    "<img align=right src=static/Aisles_Resized.png alt=Path map cannot be loaded>"\
    "<label for =cars >"\
    "<Choose a car: >" \
    "</label> "\
    "<select name = cars id = cars>"\
    "<option value = select > Select Option </option>"\
          "<option value = volvo > Volvo </option>"\
          "<option value = saab > Saab </option>"\
          "<option value = saab > Saab </option>"\
          "<option value = saab > Saab </option>"\

    "<select>"\
    """<textarea style="resize: none" rows=25 cols=40 placeholder="Be sure to check our coupons!" ></textarea>""" \
    # Import image in directory and align right. Borders?

    #Gabe yada yada 'to-do comments. Don't mind me ty
    #TODO 1 - Setup image on the right side, lined up with the "Enter your grocery list in the section below:" (Image not loading)
    #TODO 2 - Take text area input and split each line as separate element in list
    #TODO 3 - Create a top view of our store. Realistic visual, not graph visual
    #TODO 4 - Use Pillow library to draw the path from E to CO (Will find a pretier solution later)
    #TODO 5 - Add labels that are OVER the image to label what item is at each destination




    return text

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"