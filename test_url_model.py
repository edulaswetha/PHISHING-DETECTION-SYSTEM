from model_loader import url_raw_model
from utils import predict_raw_url

test_urls = [
    "http://amazon-security-check.ru/login",
    "https://google.com",
    "http://paypal.verify-account-alert.com",
    "https://github.com",
    "http://free-bitcoin-claim-now.xyz",
    "https://openai.com"
]

for url in test_urls:
    result = predict_raw_url(url_raw_model, url)
    print(f"{url}  --->  {result}")
