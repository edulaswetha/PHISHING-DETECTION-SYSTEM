import re

SUSPICIOUS_TLDS = ["xyz", "top", "ru", "tk", "ml", "ga"]

SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "suspend",
    "account",
    "immediate",
    "security",
    "password",
    "alert"
]


def extract_domain(email):
    match = re.search(r'@([a-zA-Z0-9.-]+)', email)
    return match.group(1).lower() if match else None


def analyze_email_header(header_text):
    reasons = []
    score = 0

    header_lower = header_text.lower()

    # Extract From & Reply-To
    from_match = re.search(r'from:\s*(.*)', header_lower)
    reply_match = re.search(r'reply-to:\s*(.*)', header_lower)

    from_domain = None
    reply_domain = None

    if from_match:
        from_domain = extract_domain(from_match.group(1))

    if reply_match:
        reply_domain = extract_domain(reply_match.group(1))

    # 1️⃣ Domain mismatch
    if from_domain and reply_domain and from_domain != reply_domain:
        reasons.append("From domain and Reply-To domain mismatch")
        score += 35

    # 2️⃣ Suspicious TLD
    if from_domain:
        tld = from_domain.split('.')[-1]
        if tld in SUSPICIOUS_TLDS:
            reasons.append(f"Suspicious TLD detected (. {tld})")
            score += 25

    # 3️⃣ IP address detected
    if re.search(r'\b\d{1,3}(\.\d{1,3}){3}\b', header_text):
        reasons.append("IP address found in header routing")
        score += 20

    # 4️⃣ Suspicious keywords
    for word in SUSPICIOUS_KEYWORDS:
        if word in header_lower:
            reasons.append(f"Suspicious keyword detected: '{word}'")
            score += 5

    # 5️⃣ Multiple relays
    received_count = header_lower.count("received:")
    if received_count > 3:
        reasons.append("Multiple mail relays detected")
        score += 15

    # Cap score at 100
    confidence = min(score, 100)

    # Decision threshold
    if score >= 40:
        prediction = "Phishing"
    else:
        prediction = "Legitimate"

    return prediction, confidence, reasons
