from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from routes.auth_routes import auth
from routes.kyc_routes import kyc
from utils.hash_utils import bcrypt

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS
CORS(app)

# Secret key (required for sessions / JWT if used)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize bcrypt
bcrypt.init_app(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(kyc, url_prefix="/api/kyc")


@app.route("/")
def home():
    return "Zero Backend Running 🚀"


@app.route("/health")
def health():
    return {"status": "OK"}


if __name__ == "__main__":
    # Render automatically sets PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)