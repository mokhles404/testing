
from flask import Response, request, Flask, jsonify
from flask_cors import CORS
# from Views.view import main
from Models.model import db
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"messae":"aaaaaa"})

if __name__ == '__main__':
    app.run()