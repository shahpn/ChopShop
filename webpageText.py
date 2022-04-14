from flask import Flask

app = Flask(__name__)
@app.route("/")
def home():
    text = "<title> BluPrnt </title>" \
           "<h1>Welcome To BluPrnt<h1>" \
           "<h2> Presented to you by PythonPals &#128151 Industries <h2>"
    return text

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"