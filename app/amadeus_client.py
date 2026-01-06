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

    # lấy token hoặc dùng token cũ nếu còn hạn
    def get_access_token(self):      
        #Đúng token còn hạn thì dùng lại  
        if self.token != None and time.time() < self.token_expiry:
            return self.token
        
        #Lấy url từ OAuth2 (agrument lấy token)
        url = f"{self.base_url}/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }

        try:
            #gửi POST(api method) xin token 
            res = requests.post(url, data=data)
            res.raise_for_status()      #exception
        except requests.HTTPError as e:
            print(f"❌ Token authentication failed: {e}")
            raise

        #lưu token
        token_data = res.json()
        self.token = token_data["access_token"]
        self.token_expiry = time.time() + token_data["expires_in"] - 60

        return self.token
    
    #gọi bất kì API GET nào của Amadeus
    def get(self, endpoint, params=None):

        #get token
        token = self.get_access_token() 

        #Header bắt buộc của Amadeus
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        url = f"{self.base_url}{endpoint}"

        #gửi GET request
        try:
            res = requests.get(url, headers=headers, params=params)
            res.raise_for_status() #exception 
        except requests.HTTPError as e:
            print(f"❌ API request failed: {e}")
            if res.status_code == 400:
                print(f"Response: {res.json()}")
            raise

        return res.json().get("data", [])
    
    def price_offers(self, offers, max_batch = 6):
        token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Chỉ lấy tối đa 6 offers (giới hạn của Amadeus)
        batch = offers[:6] 

        payload = {
            "data": {
            "type": "flight-offers-pricing",
            "flightOffers": batch  # Gửi nhiều offers cùng lúc
            }
        }

        try:
            #request syntax: request.posts("url", headers, json)
            r = requests.post(f"{self.base_url}/v1/shopping/flight-offers/pricing",headers=headers,json=payload)
            r.raise_for_status()

        except requests.HTTPError as e:
            print(f"❌ Pricing failed: {e}")
            if r.status_code == 400:
                print(f"Response: {r.json()}")
            raise

        return r.json()["data"]["flightOffers"]

