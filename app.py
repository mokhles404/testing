
from flask import Response, request, Flask, jsonify


app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"messae":"heloooo"})

if __name__ == '__main__':
    app.run()