from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth
from routes.kyc_routes import kyc
from utils.hash_utils import bcrypt

app = Flask(__name__)
CORS(app)

bcrypt.init_app(app)

app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(kyc, url_prefix="/api/kyc")

@app.route("/")
def home():
    return "Zero Backend Running 🚀"

@app.route("/test", methods=["GET"])
def test():
    return "Test route working"

if __name__ == "__main__":
    app.run()