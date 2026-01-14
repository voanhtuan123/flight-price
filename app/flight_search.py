from app.amadeus_client import AmadeusClient

from datetime import datetime

def is_published_fare(offer):
    pricing = offer.get("pricingOptions", {})
    fare_types = pricing.get("fareType", [])
    return "PUBLISHED" in fare_types

def search_flights(origin, destination, date, adults=1, max_results=5,):
    #tạo object client (tự động tạo token)
    client = AmadeusClient()

    #các agrument để search 
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "currencyCode": "CAD",
        "max": max_results,
    }

   # Gọi API search flight đến Amadeus
    offers = client.get("/v2/shopping/flight-offers", params=params)

    # Kiểm tra nếu không có kết quả
    if not offers:
        print(" No flights found for this route")
        return []

    #trả về list 
    published_offers = [
        o for o in offers if is_published_fare(o)
    ]

    #Nếu không có published fare, dùng tất cả offers
    if not published_offers:
        print("⚠️ No published fares found, using all available offers")
        published_offers = offers


#Dùng unified pricing method (handle cả 1 và nhiều offers)
    try:
        priced_offers = client.price_offers(published_offers)
        print(f"✅ Successfully priced {len(priced_offers)} offers")
    except Exception as e:
        print(f"⚠️ Pricing failed: {e}")
        return []

    # Kiểm tra nếu không có offer nào được price thành công
    if not priced_offers:
        print("❌ No offers could be priced")
        return []

    # Sort theo giá cuối (grandTotal)
    priced_offers.sort(
        key=lambda o: float(o["price"]["grandTotal"])
    )

    exact_match = []
    nearby_airports = []
    
    for offer in priced_offers:
        final_destination = offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        
        if final_destination == destination:
            exact_match.append(offer)
        else:
            nearby_airports.append(offer)
    
    # Ưu tiên exact match, nếu không có thì dùng nearby
    if exact_match:
        priced_offers = exact_match
        print(f"📍 Showing {len(priced_offers)} flights to {destination}")
    else:
        priced_offers = nearby_airports
        print(f"⚠️ No flights to {destination}, showing {len(priced_offers)} flights to nearby airports")
    
    if not priced_offers:
        print("❌ No offers available after filtering")
        return []
     

    return priced_offers
