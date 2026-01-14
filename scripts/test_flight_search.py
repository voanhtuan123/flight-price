from app.flight_search import search_flights
from datetime import datetime

# Import agruments 
data = search_flights(
    origin="YYC",
    destination="YVR",
    date="2026-03-15",
    max_results=20,   
)

for offer in data:
    price = offer["price"]["grandTotal"]
    currency = offer["price"]["currency"]
    print(f"Price: {price} {currency}")
    
    # 🔧 FIX: Lấy duration hoặc tính thủ công nếu không có
    itinerary = offer["itineraries"][0]
    duration = itinerary.get("duration")
    
    if not duration:
        # Tính duration từ departure đầu tiên → arrival cuối cùng
        segments = itinerary["segments"]
        start = datetime.fromisoformat(segments[0]["departure"]["at"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(segments[-1]["arrival"]["at"].replace("Z", "+00:00"))
        total_seconds = int((end - start).total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        duration = f"PT{hours}H{minutes}M"
    
    print("Duration: ", duration)
    
    for segment in itinerary["segments"]:
        print(
            segment["carrierCode"],
            segment["number"],
            segment["departure"]["iataCode"],
            "→",
            segment["arrival"]["iataCode"],
            segment["departure"]["at"]
        )
    
    print("-----")