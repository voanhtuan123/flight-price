import os 
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class AmadeusClient:
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.base_url = "https://test.api.amadeus.com"
        self.token = None
        self.token_expiry = 0

    #get token, reuse if valid, otherwise request new token
    def get_access_token(self):      
        #reuse token if valid 
        if self.token != None and time.time() < self.token_expiry:
            return self.token
        
        #request new token
        url = f"{self.base_url}/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }

        #send POST request to get token 
        res = requests.post(url, data=data)
        if res.status_code != 200:
            print("Amadeus error response:")
            print(res.text)
            res.raise_for_status()


        #parse token response
        token_data = res.json()
        self.token = token_data["access_token"]
        self.token_expiry = time.time() + token_data["expires_in"] - 60

        return self.token
    
    #send GET request to Amadeus API with authorization header
    def get(self, endpoint, params=None):

        #get token
        token = self.get_access_token() 

        #set authorization header
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        url = f"{self.base_url}{endpoint}"

        #send GET request
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200:
            print("Amadeus error response:")
            print(res.text)
            res.raise_for_status()
        return res.json()