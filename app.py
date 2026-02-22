# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# import io
# import hashlib
# import numpy as np
# import PIL.Image
# import face_recognition

# from routes.auth_routes import auth
# from routes.kyc_routes import kyc
# from utils.hash_utils import bcrypt

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)

# # Enable CORS
# CORS(app)

# # Secret key (required for sessions / JWT if used)
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# # Initialize bcrypt
# bcrypt.init_app(app)

# # Register Blueprints
# app.register_blueprint(auth, url_prefix="/api/auth")
# app.register_blueprint(kyc, url_prefix="/api/kyc")

# def extract_embedding(image_bytes: bytes) -> np.ndarray:
#     pil_image = PIL.Image.open(io.BytesIO(image_bytes)).convert('RGB')
#     w, h = pil_image.size
#     if w > 800:
#         ratio = 800 / w
#         pil_image = pil_image.resize((800, int(h * ratio)), PIL.Image.LANCZOS)
#     img_array = np.array(pil_image)
#     face_locations = face_recognition.face_locations(img_array, model='hog')
#     if len(face_locations) == 0:
#         face_locations = face_recognition.face_locations(img_array, number_of_times_to_upsample=2, model='hog')
#     if len(face_locations) == 0:
#         raise ValueError("No face detected. Ensure your face is clearly visible and well-lit.")
#     if len(face_locations) > 1:
#         face_locations = [max(face_locations, key=lambda f: (f[2]-f[0]) * (f[1]-f[3]))]
#     encodings = face_recognition.face_encodings(img_array, known_face_locations=face_locations, num_jitters=1)
#     if not encodings:
#         raise ValueError("Could not encode face. Please try again with better lighting.")
#     return np.array(encodings[0])

# def face_distance(a: np.ndarray, b: np.ndarray) -> float:
#     return float(np.linalg.norm(a - b))

# def check_duplicate(new_embedding: np.ndarray, exclude_wallet: str = None) -> dict | None:
#     DUPLICATE_THRESHOLD = 0.5
#     for wallet, data in enrolled_faces.items():
#         if wallet == exclude_wallet:
#             continue
#         existing = np.array(data['embedding'])
#         dist = face_distance(new_embedding, existing)
#         if dist < DUPLICATE_THRESHOLD:
#             return {'conflicting_wallet': wallet[:8] + '...' + wallet[-4:], 'distance': round(dist, 4)}
#     return None

# def compute_face_hash(embedding: np.ndarray) -> str:
#     return '0x' + hashlib.sha3_256(embedding.tobytes()).hexdigest()
# @app.route("/")
# def home():
#     return "Zero Backend Running 🚀"


# @app.route("/health")
# def health():
#     return {"status": "OK"}

# @app.post('/api/enroll-face')
# async def enroll_face(selfie: UploadFile = File(...), walletAddress: str = Form(...)):
#     image_bytes = await selfie.read()
#     if len(image_bytes) < 5000:
#         raise HTTPException(status_code=400, detail='Image too small')

#     try:
#         embedding = extract_embedding(image_bytes)
#     except ValueError as e:
#         raise HTTPException(status_code=422, detail=str(e))

#     new_embedding_arr = np.array(embedding)

#     # Duplicate check — no await with pymongo
#     all_enrolled = list(db.face_enrollments.find({}, {"wallet": 1, "embedding": 1}))
#     for record in all_enrolled:
#         if record["wallet"] == walletAddress:
#             continue
#         existing = np.array(record["embedding"])
#         dist = face_distance(new_embedding_arr, existing)
#         if dist < 0.5:
#             raise HTTPException(status_code=409, detail={
#                 'error': 'DUPLICATE_FACE',
#                 'message': 'Face already enrolled under another wallet.',
#                 'distance': round(dist, 4),
#             })

#     embedding_hash = compute_face_hash(new_embedding_arr)

#     # Upsert — no await with pymongo
#     db.face_enrollments.update_one(
#         {"wallet": walletAddress},
#         {"$set": {
#             "wallet": walletAddress,
#             "embedding": embedding.tolist(),
#             "embedding_hash": embedding_hash,
#             "enrolled_at": int(time.time()),
#             "model": "dlib face_recognition",
#         }},
#         upsert=True
#     )

#     del image_bytes
#     return JSONResponse({'success': True, 'embeddingHash': embedding_hash})


# @app.post('/api/verify-face')
# async def verify_face(selfie: UploadFile = File(...), walletAddress: str = Form(...)):
#     # Fetch from MongoDB — no await with pymongo
#     record = db.face_enrollments.find_one({"wallet": walletAddress})
#     if not record:
#         raise HTTPException(status_code=404, detail='Wallet not enrolled. Complete face enrollment first.')

#     stored_embedding = np.array(record["embedding"])

#     image_bytes = await selfie.read()
#     if len(image_bytes) < 5000:
#         raise HTTPException(status_code=400, detail='Image too small')

#     try:
#         new_embedding = extract_embedding(image_bytes)
#     except ValueError as e:
#         raise HTTPException(status_code=422, detail=str(e))

#     distance = face_distance(new_embedding, stored_embedding)
#     matched = distance < 0.6
#     confidence = round(max(0.0, (1.0 - distance / 0.6) * 100), 2)

#     del image_bytes, new_embedding
#     return {
#         'matched': matched,
#         'confidence': confidence,
#         'raw_distance': round(distance, 4),
#         'status': 'VERIFIED' if matched else 'MISMATCH',
#     }
# if __name__ == "__main__":
#     # Render automatically sets PORT
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=True)

#version 2
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from routes.auth_routes import auth
from routes.kyc_routes import kyc
from routes.dashboard_routes import dashboard
from utils.hash_utils import bcrypt
from config import db   # ← using your existing MongoDB connection

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS
CORS(app)

# Secret key
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize bcrypt
bcrypt.init_app(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(kyc, url_prefix="/api/kyc")
app.register_blueprint(dashboard, url_prefix="/api/dashboard")

# ───────────────── BASIC ROUTES ─────────────────

@app.route("/")
def home():
    return "Zero Backend Running 🚀"


@app.route("/health")
def health():
    return jsonify({"status": "OK"})


# ───────────────── RUN APP ─────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)