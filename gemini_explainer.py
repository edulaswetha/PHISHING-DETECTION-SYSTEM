from google import genai

# Create client (AI Studio key)
client = genai.Client(
    api_key="AIzaSyD7VLPITTB3bQkcaBuP1Ndb23a7m_FTLnE"
)

def generate_explanation(text, prediction, confidence, reasons):

    prompt = f"""
You are a cybersecurity expert.

Analyze the following detection result:

Text:
{text}

Prediction:
{prediction}

Confidence:
{confidence}%

Reasons:
{reasons}

Explain clearly:
1. Why this was classified as phishing or legitimate.
2. What risk level it represents.
3. What  should you do next.

Keep explanation short and practical.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"
