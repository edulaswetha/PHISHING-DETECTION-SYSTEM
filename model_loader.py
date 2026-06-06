import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------
# Model Paths
# -----------------------------
EMAIL_MODEL_PATH = os.path.join(BASE_DIR, "ml", "email_model.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "ml", "tfidf_vectorizer.pkl")

# Active URL model (feature-based)
URL_RAW_MODEL_PATH = os.path.join(BASE_DIR, "ml", "url_raw_model.pkl")

email_model = joblib.load(EMAIL_MODEL_PATH)
tfidf_vectorizer = joblib.load(TFIDF_PATH)

# Single Active URL Model
url_raw_model = joblib.load(URL_RAW_MODEL_PATH)

print("✅ All models loaded successfully")
