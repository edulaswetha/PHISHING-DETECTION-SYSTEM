from pyexpat import features
import sys
import os
import re
import pandas as pd
from urllib.parse import urlparse

# -----------------------------
# Path setup to access ml folder
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "ml")
sys.path.append(ML_DIR)

# Old feature extraction (kept for reference / future use)
from feature_extraction import extract_url_features

# -----------------------------
# EMAIL PREDICTION (UNCHANGED)
# -----------------------------
def predict_email(model, vectorizer, email_text):
    X = vectorizer.transform([email_text])
    pred = model.predict(X)[0]
    return "Phishing" if pred == 1 else "Legitimate"

def predict_sms(model, vectorizer, sms_text):
    sms_text = sms_text.strip()

    # Very short SMS safety rule
    if len(sms_text.split()) <= 4:
        return "Legitimate", 50.0

    X = vectorizer.transform([sms_text])

    prob = model.predict_proba(X)[0]
    phishing_prob = prob[1]
    legitimate_prob = prob[0]

    confidence = round(max(prob) * 100, 2)

    # Adjusted threshold (more strict)
    if phishing_prob >= 0.75:
        prediction = "Phishing"
    else:
        prediction = "Legitimate"

    return prediction, confidence



# -----------------------------
# OLD URL PREDICTION (FEATURE-BASED)
# Kept for documentation / viva
# -----------------------------
def predict_url_feature_based(model, url):
    features = extract_url_features(url)
    X = pd.DataFrame([features])
    pred = model.predict(X)[0]
    return "Phishing" if pred == 1 else "Legitimate"

# -----------------------------
# RAW URL FEATURE EXTRACTION (NEW)
# -----------------------------
def extract_raw_url_features(url):
    url = str(url)

    features = {}
    features["url_length"] = len(url)
    features["count_dots"] = url.count(".")
    features["count_hyphen"] = url.count("-")
    features["count_at"] = url.count("@")
    features["count_question"] = url.count("?")
    features["count_slash"] = url.count("/")
    features["count_equals"] = url.count("=")
    features["count_digits"] = sum(c.isdigit() for c in url)

    features["has_https"] = 1 if url.startswith("https") else 0
    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0

    suspicious_words = [
        "login", "secure", "account", "verify",
        "update", "bank", "paypal", "free"
    ]
    features["suspicious_words"] = sum(
        word in url.lower() for word in suspicious_words
    )

    parsed = urlparse(url)
    features["domain_length"] = len(parsed.netloc)
    features["subdomain_count"] = parsed.netloc.count(".")

    return pd.DataFrame([features])

# -----------------------------
# RAW URL PREDICTION (ACTIVE)
# -----------------------------
def predict_raw_url(model, url):
    url_lower = url.lower()

    # -----------------------------
    # Heuristic layer (fast & strong)
    # -----------------------------
    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "account", "bank", "paypal", "free",
        "gift", "confirm"
    ]

    if any(word in url_lower for word in suspicious_keywords):
        return "Phishing"

    # -----------------------------
    # ML prediction layer
    # -----------------------------
    features = extract_url_features(url)
    X = pd.DataFrame([features])
    pred = model.predict(X)[0]

    return "Phishing" if pred == 1 else "Legitimate"
