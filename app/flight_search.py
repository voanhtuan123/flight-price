from app.amadeus_client import AmadeusClient

def is_published_fare(offer):
    pricing = offer.get("pricingOptions", {})
    fare_types = pricing.get("fareType", [])
    return "PUBLISHED" in fare_types

def search_flights(origin, destination, date, adults=1, max_results=5):
    #tạo object client (tự động tạo token)
    client = AmadeusClient()

    #các agrument để search 
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "currencyCode": "CAD",
        "max": max_results
    }

    #gọi API search flight đến Amadeus
    data = client.get("/v2/shopping/flight-offers", params=params)
    offers = data.get("data", [])

    #FIX: Kiểm tra nếu không có kết quả
    if not offers:
        print(" No flights found for this route")
        return []

    #trả về list 
    published_offers = [
        o for o in offers if is_published_fare(o)
    ]

    #FIX: Nếu không có published fare, dùng tất cả offers
    if not published_offers:
        print("⚠️ No published fares found, using all available offers")
        published_offers = offers

    
    return published_offers   #trả về list, không còn là json 
