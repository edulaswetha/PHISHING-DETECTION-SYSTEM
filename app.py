from flask import Flask, request, jsonify, send_from_directory
from header_analyzer import analyze_email_header
from gemini_explainer import generate_explanation
from database import init_db
from flask import session
from flask_bcrypt import Bcrypt
from database import get_db_connection
from flask_cors import CORS
import os


app = Flask(__name__)
app.secret_key = "phishguard_secure_key_2026"

CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)

# -----------------------------
# Paths (DO NOT CHANGE STRUCTURE)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# -----------------------------
# Load models
# -----------------------------
from model_loader import (
    email_model,
    tfidf_vectorizer,
    url_raw_model
)

# -----------------------------
# Import prediction utilities
# -----------------------------
from utils import (
    predict_email,
    predict_raw_url,
    predict_sms
)

# =============================
# FRONTEND ROUTES
# =============================

@app.route("/")
def landing_page():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/detect")
def detect_page():
    return send_from_directory(FRONTEND_DIR, "detect.html")

@app.route("/chat")
def chat_page():
    return send_from_directory(FRONTEND_DIR, "chat.html")


@app.route("/login")
def login_page():
    return send_from_directory(FRONTEND_DIR, "login.html")


@app.route("/signup")
def signup_page():
    return send_from_directory(FRONTEND_DIR, "signup.html")


# Serve CSS files
@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)


# Serve JS and other static frontend files
@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# =============================
# API ROUTES
# =============================

# Email phishing detection
@app.route("/check-email", methods=["POST"])
def check_email():
    data = request.json
    email_text = data.get("email", "")

    if not email_text:
        return jsonify({"error": "Email text is required"}), 400

    result = predict_email(email_model, tfidf_vectorizer, email_text)
    return jsonify({"prediction": result})

# -----------------------------
# SMS phishing detection
# -----------------------------
@app.route("/check-sms", methods=["POST"])
def check_sms():
    data = request.json
    sms_text = data.get("sms", "")

    if not sms_text:
        return jsonify({"error": "SMS text is required"}), 400

    result, confidence = predict_sms(email_model, tfidf_vectorizer, sms_text)

    return jsonify({
        "prediction": result,
        "confidence": confidence
    })

# -----------------------------
# Email Header Detection
# -----------------------------
@app.route("/check-header", methods=["POST"])
def check_header():
    data = request.json
    header_text = data.get("header", "")

    if not header_text:
        return jsonify({"error": "Header text is required"}), 400

    prediction, confidence, reasons = analyze_email_header(header_text)

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "reasons": reasons
    })


# URL phishing detection (RAW URL MODEL)
@app.route("/check-url", methods=["POST"])
def check_url():
    data = request.json
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = predict_raw_url(url_raw_model, url)
    return jsonify({"prediction": result})

# -----------------------------
# Unified Chat Analysis Endpoint
# -----------------------------
@app.route("/analyze-chat", methods=["POST"])
def analyze_chat():
    try:
        data = request.json
        input_text = data.get("text", "")
        mode = data.get("mode", "sms")

        if not input_text:
            return jsonify({"error": "Input text required"}), 400

        if mode == "sms":
            prediction, confidence = predict_sms(email_model, tfidf_vectorizer, input_text)
            reasons = []

        elif mode == "email":
            prediction = predict_email(email_model, tfidf_vectorizer, input_text)
            confidence = 0
            reasons = []

        elif mode == "url":
            prediction = predict_raw_url(url_raw_model, input_text)
            confidence = 0
            reasons = []

        elif mode == "header":
            prediction, confidence, reasons = analyze_email_header(input_text)

        else:
            return jsonify({"error": "Invalid mode"}), 400

        explanation = generate_explanation(
            input_text,
            prediction,
            confidence,
            reasons
        )

        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "reasons": reasons,
            "explanation": explanation
        })

    except Exception as e:
        print("ANALYZE ERROR:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route("/signup-user", methods=["POST"])
def signup_user():
    data = request.json
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "User created successfully"})

    except Exception as e:
        return jsonify({"error": "Username or Email already exists"}), 400
    
@app.route("/login-user", methods=["POST"])
def login_user():
    data = request.json
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/logout-user")
def logout_user():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route("/get-user")
def get_user():
    if "user_id" in session:
        return jsonify({
            "logged_in": True,
            "username": session.get("username")
        })
    return jsonify({"logged_in": False})


    # =============================
    # AUTO DETECT MODE
    # =============================

    # Detect URL automatically
    if re.match(r"^https?://", input_text):
        mode = "url"
    else:
        mode = data.get("mode", "sms")  # fallback

    # =============================
    # DETECTION LOGIC
    # =============================

    if mode == "sms":
        prediction, confidence = predict_sms(
            email_model, tfidf_vectorizer, input_text
        )
        reasons = []

    elif mode == "email":
        prediction = predict_email(
            email_model, tfidf_vectorizer, input_text
        )
        confidence = 0
        reasons = []

    elif mode == "url":
        print("DEBUG: URL mode triggered")
        print("DEBUG: URL received:", input_text)

        prediction = predict_raw_url(
            url_raw_model, input_text
        )

        print("DEBUG: Prediction from model:", prediction)

        confidence = 90  # you can adjust if needed
        reasons = []

    elif mode == "header":
        prediction, confidence, reasons = analyze_email_header(input_text)

    else:
        return jsonify({"error": "Invalid mode"}), 400

    # =============================
    # AI Explanation
    # =============================

    explanation = generate_explanation(
        input_text,
        prediction,
        confidence,
        reasons
    )

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "reasons": reasons,
        "explanation": explanation
    })

    # =============================
    # AI Explanation
    # =============================

    explanation = generate_explanation(
        input_text,
        prediction,
        confidence,
        reasons
    )

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "reasons": reasons,
        "explanation": explanation
    })

# -----------------------------
# AI Explanation Endpoint
# -----------------------------
@app.route("/generate-explanation", methods=["POST"])
def generate_ai_explanation():
    data = request.json

    input_text = data.get("text", "")
    prediction = data.get("prediction", "")
    confidence = data.get("confidence", "")
    reasons = data.get("reasons", [])

    if not input_text:
        return jsonify({"error": "Input text required"}), 400

    explanation = generate_explanation(
        input_text,
        prediction,
        confidence,
        reasons
    )

    return jsonify({
        "explanation": explanation
    })



# =============================
# RUN SERVER
# =============================
if __name__ == "__main__":
    app.run(debug=True)
