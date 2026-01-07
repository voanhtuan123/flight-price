import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.flight_search import search_flights

def weekly_check():
    """Run weekly flight checks for preset routes"""
    
    print(f"\n{'='*60}")
    print(f"Flight Price Check - {datetime.now()}")
    print(f"{'='*60}\n")
    
    # Routes you want to monitor (customize these!)
    routes = [
        {"origin": "YYC", "destination": "HAN", "name": "Calgary to Hanoi"},
        {"origin": "YYC", "destination": "SGN", "name": "Calgary to Saigon"},
        # Add more routes here
    ]
    
    # Check flights for April 30, 2026
    departure_date = "2026-04-30"
    
    for route in routes:
        print(f"\n📍 Checking: {route['name']}")
        print(f"   Departure Date: {departure_date}")
        print("-" * 60)
        
        try:
            offers = search_flights(
                origin=route['origin'],
                destination=route['destination'],
                date=departure_date,
                adults=1,
                max_results=5
            )
            
            if offers:
                cheapest = min(offers, key=lambda x: float(x['price']['total']))
                price = cheapest['price']
                print(f"✅ Found {len(offers)} flights")
                print(f"💰 Cheapest: {price['total']} {price['currency']}")
                
                # Show all prices
                print(f"\nAll offers:")
                for i, offer in enumerate(offers, 1):
                    p = offer['price']
                    itinerary = offer['itineraries'][0]
                    stops = len(itinerary['segments']) - 1
                    print(f"  {i}. {p['total']} {p['currency']} - {stops} stop(s)")
            else:
                print("⚠️  No flights found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Weekly check completed!")
    print(f"Data saved to PostgreSQL database")
    print(f"View in pgAdmin 4: flight_prices table")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    weekly_check()