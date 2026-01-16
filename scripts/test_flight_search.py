from app.flight_search import search_flights

#import agruments 
data = search_flights(
    origin="YYC",
    destination="HAN",
    date="2026-03-15",
)

for offer in data:
    price = offer["price"]["total"]
    currency = offer["price"]["currency"]
    print(f"Price: {price} {currency}")
    duration = offer["itineraries"][0]["duration"]
    print("Duration: ", duration)

    for segment in offer["itineraries"][0]["segments"]:
        print(
            segment["carrierCode"],
            segment["number"],
            segment["departure"]["iataCode"],
            "→",
            segment["arrival"]["iataCode"],
            segment["departure"]["at"]
        )
    print("-----")
