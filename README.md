Phishguard-AI-Phishing-Detection
AI-based phishing detection system using Flask & ML (URL, Email, SMS, Header analysis with explanation)

PhishGuard — AI-Based Phishing Detection System
PhishGuard is a full-stack AI-powered phishing detection system designed to protect users from modern cyber threats. It analyzes URLs, emails, SMS messages, and email headers to determine whether the content is phishing or legitimate.

The system combines Machine Learning, Cybersecurity principles, and Web Technologies to provide accurate detection along with a clear explanation, helping users understand the risk before taking action.

Project Overview
Phishing attacks are one of the most common cyber threats today. Users often lose sensitive information such as passwords, banking details, and personal data by clicking malicious links or trusting fake messages.

PhishGuard solves this problem by providing:

Real-time phishing detection
Multi-input analysis (URL, Email, SMS, Header)
AI-based explanation for better understanding
Optional user authentication system
This project demonstrates how AI can be used to improve cybersecurity awareness and protect users in real-world scenarios.

Key Features
URL Phishing Detection Detects malicious URLs using feature-based machine learning

Email Analysis Identifies phishing emails using NLP techniques

SMS Scam Detection Detects fraud messages based on patterns and keywords

Email Header Analysis Checks sender authenticity and routing issues

AI-Based Explanation Provides human-readable reasoning behind predictions

Real-Time Results Fast and interactive detection system

Authentication System (Optional) Users can sign up and log in securely

Modern UI Clean interface with animations (Vanta.js)

Technologies Used
Frontend
HTML5
CSS3
JavaScript
Vanta.js (for animated background)
Backend
Python
Flask
Machine Learning
Scikit-learn
XGBoost
TF-IDF Vectorization
Pandas
NumPy
Database
SQLite
Flask-Bcrypt (for password hashing)
⚙️ How the System Works
User inputs data (URL / Email / SMS / Header)
Frontend sends request to Flask backend
Backend processes the input
Feature extraction is performed
Machine learning model predicts the result
AI explanation is generated
Result is displayed with confidence score
Project Structure
Phishing-Detection-System/
│
├── backend/
│   ├── app.py
│   ├── model_loader.py
│   ├── utils.py
│   ├── database.py
│   ├── gemini_explainer.py
│   ├── header_analyzer.py
│
├── frontend/
│   ├── index.html
│   ├── detect.html
│   ├── login.html
│   ├── signup.html
│   ├── script.js
│   ├── css/
│
├── ml/
│   ├── url_model.pkl
│   ├── url_raw_model.pkl
│   ├── email_model.pkl
│   ├── tfidf_vectorizer.pkl
│
├── datasets/
│   ├── phishing_urls.csv
│
└── README.md
Example
Input:

http://free-bitcoin-claim-now.xyz
Output:

Phishing (High Confidence)
Reason: Suspicious keywords + abnormal URL structure
Model Performance
Accuracy: ~90%

Algorithms Used:

Random Forest
XGBoost
The models are trained using real-world phishing datasets and optimized for better accuracy.

Authentication
Secure login and signup system
Passwords stored using hashing (bcrypt)
Session-based authentication
Optional usage (system works without login)
Future Improvements
Deep learning models (LSTM / Transformers)
Browser extension for real-time detection
Mobile application (Android/iOS)
Integration with APIs like Google Safe Browsing
Cloud deployment for scalability
Team
Dheeraj Gandesri
Spandana Reddy
Srinathu Charan Santosh
Edula Swetha
Output Screens
Landing page Description page Services page About page Input page Output page Output page (2)

License
This project is developed for academic and educational purposes.

Support
If you found this project useful, consider giving it a ⭐ on GitHub!
