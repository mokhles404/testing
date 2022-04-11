
from flask import Response, request, Flask, jsonify, make_response
from flask_cors import CORS
from Views.view import main
from Models.model import db
from werkzeug.serving import WSGIRequestHandler


app = Flask(__name__)
app.register_blueprint(main)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carrot.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretcarrot'
CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

WSGIRequestHandler.protocol_version = "HTTP/1.1"

@app.route("/")
def index():
    return jsonify({"messae":"heloooo"})

if __name__ == '__main__':
    app.run()         