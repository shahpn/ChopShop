from flask import Flask

app = Flask(__name__)
@app.route("/")
def home():
    text ="<head>"\
    "<style>"\
    "h1 {text-align: center;}"\
    "h2 {text-align: center;}" \
    "p {text-align: center;}"\
    "div {text-align: center;}"\
    "</style>"\
    "</head>"\
    "<body>" \
    "<body style=background-color:powderblue;>" \
    "<title> BluPrnt </title>" \
    "<h1>Welcome To BluPrnt<h1>" \
    "<h2> Presented to you by PythonPals &#128151 Industries <h2>"\
    "<p> Enter your grocery list in the section below: <p>"
    return text

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"