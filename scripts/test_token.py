import os
import requests
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

if not API_KEY or not API_SECRET:
    raise Exception("Missing API key or secret")

url = "https://test.api.amadeus.com/v1/security/oauth2/token"

data = {
    "grant_type": "client_credentials",
    "client_id": API_KEY,
    "client_secret": API_SECRET
}

response = requests.post(url, data=data)

print("Status code:", response.status_code)
print("Response JSON:")
print(response.json())
