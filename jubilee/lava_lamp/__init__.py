# Package import
from flask import Flask, render_template, send_file, make_response, url_for, Response, redirect, request

# initialise app
app = Flask(__name__)


# decorator for homepage
@app.route('/')
def index():
    return render_template('index.html', PageTitle="Landing page")


# These functions will run when POST method is used.
@app.route('/foo', methods=["POST"])
def plot_png():
    slide_value = request.json['slide_value']
    print(f"moo: {slide_value}")
    return "woo"


if __name__ == '__main__':
    app.run(debug=True)


