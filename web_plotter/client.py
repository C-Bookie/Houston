from flask import Flask, render_template

app = Flask(__name__)


# index
@app.route('/')
def index():
    with open("index.html", 'r') as file:
        return file.read()

# index
@app.route('/transponder.js')
def get_transponder():
    with open("transponder.js", 'r') as file:
        return file.read()


# /me
@app.route("/me", methods=["GET"])
def get_results():
    return "Dummy Result"


if __name__ == "__main__":
    app.run()
