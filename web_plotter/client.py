from flask import Flask, request, jsonify

app = Flask(__name__)


# index
@app.route('/')
def index():
    with open("index.html", 'r') as file:
        return file.read(), 200

# index
@app.route('/transponder.js')
def get_transponder():
    with open("transponder.js", 'r') as file:
        return file.read(), 200


# /me
@app.route("/test", methods=["POST"])
def post_test():
    if request.method == 'POST':
        foo = request.form.get('foo')
        bar = int(request.form.get('bar'))
    else:
        foo = 'hmm'
        bar = 0

    bar *= 2

    return jsonify(
        method=request.method,
        foo=foo,
        bar=bar
    ), 200


if __name__ == "__main__":
    app.run()
