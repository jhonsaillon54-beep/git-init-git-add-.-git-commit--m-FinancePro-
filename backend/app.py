from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

# Rotas
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return {"message": "FinancePro API Online"}

if __name__ == "__main__":
    app.run(debug=True)