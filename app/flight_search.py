from app.amadeus_client import AmadeusClient
from datetime import datetime

def is_published_fare(offer):
    pricing = offer.get("pricingOptions", {})
    fare_types = pricing.get("fareType", [])
    return "PUBLISHED" in fare_types


def search_flights(origin, destination, date, adults=1, max_results=5):
    # tạo object client (tự động tạo token)
    client = AmadeusClient()
    
    # set params cho API request
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "currencyCode": "CAD",
        "max": max_results
    }
    
    # call API search flight to Amadeus
    data = client.get("/v2/shopping/flight-offers", params=params)
    offers = data.get("data", [])
    
    # return LIST TYPE of flight offers with PUBLISHED fare type only
    published_offers = [
        o for o in offers if is_published_fare(o)
    ]
    
    return published_offers  