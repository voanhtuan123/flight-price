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

    return priced_offers
