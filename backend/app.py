from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
from flask_cors import CORS

CORS(app)

from routes.auth import auth_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")