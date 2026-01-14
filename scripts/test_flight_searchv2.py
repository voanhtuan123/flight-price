from app.flight_search import search_flights
from datetime import datetime

# Test với nhiều routes khác nhau
test_routes = [
    {"origin": "YYC", "destination": "YVR", "name": "Calgary → Vancouver"},
    {"origin": "YYC", "destination": "HAN", "name": "Calgary → Hanoi"},
    {"origin": "YYC", "destination": "YYZ", "name": "Calgary → Toronto"},
]

for route in test_routes:
    print(f"\n{'='*70}")
    print(f"🔍 {route['name']}")
    print(f"{'='*70}\n")
    
    try:
        data = search_flights(
            origin=route["origin"],
            destination=route["destination"],
            date="2026-01-15",
        )

        if not data:
            print(f"❌ No offers for {route['name']}\n")
            continue

        print(f"Found {len(data)} options:\n")

        for i, offer in enumerate(data, 1):
            price = offer["price"]["grandTotal"]
            currency = offer["price"]["currency"]
            
            # Confidence level
            confidence = offer.get("_price_confidence", "ESTIMATED")
            confidence_emoji = {
                "HIGH": "🟢",
                "MEDIUM": "🟡", 
                "ESTIMATED": "🟠"
            }.get(confidence, "⚪")
            
            itinerary = offer["itineraries"][0]
            
            # Get duration
            duration = itinerary.get("duration")
            if not duration:
                segments = itinerary["segments"]
                start = datetime.fromisoformat(segments[0]["departure"]["at"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(segments[-1]["arrival"]["at"].replace("Z", "+00:00"))
                total_seconds = int((end - start).total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                duration = f"PT{hours}H{minutes}M"
            
            segments = itinerary["segments"]
            
            print(f"{'─'*60}")
            print(f"Option {i}: {price} {currency} {confidence_emoji} {confidence}")
            print(f"{'─'*60}")
            print(f"Duration: {duration}")
            print(f"Stops: {len(segments) - 1}")
            print()
            
            for j, seg in enumerate(segments, 1):
                print(
                    f"  Leg {j}: {seg['carrierCode']}{seg['number']:>4}  "
                    f"{seg['departure']['iataCode']} → {seg['arrival']['iataCode']}  "
                    f"{seg['departure']['at']}"
                )
            
            # 🔗 IN RA BOOKING LINKS
            booking_links = offer.get("_booking_links")
            if booking_links:
                print()
                print(f"🔗 Book this flight:")
                print(f"   {booking_links['primary']}")
                
                # Uncomment để show tất cả options:
                # print(f"\n   📍 All booking options:")
                # print(f"      Airline: {booking_links['airline']}")
                # print(f"      Google:  {booking_links['google']}")
            else:
                print()
                print("⚠️  Booking links not generated")
            
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()

print("="*70)
print("💡 Prices are from Search API (estimated, typically 90-95% accurate)")
print("💡 Click booking links to see final prices and complete purchase")
print("="*70)