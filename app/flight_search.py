from app.amadeus_client import AmadeusClient
from app.db.database import SessionLocal
from app.db.table_models import FlightSearch, FlightPrice
from datetime import datetime

def is_published_fare(offer):
    pricing = offer.get("pricingOptions", {})
    fare_types = pricing.get("fareType", [])
    return "PUBLISHED" in fare_types

# def save_flight_data(origin, destination, date, adults, offers):
#     """Save flight search and prices to database"""
#     db = SessionLocal()
#     try:
#         # Create flight search record
#         search = FlightSearch(
#             origin=origin,
#             destination=destination,
#             departure_date=datetime.strptime(date, "%Y-%m-%d").date(),
#             adults=adults
#         )
#         db.add(search)
#         db.flush()
        
#         print(f"💾 Saving {len(offers)} flight offers...")
        
#         # Save each flight offer
#         for offer in offers:
#             itinerary = offer.get('itineraries', [{}])[0]
#             segments = itinerary.get('segments', [])
            
#             if segments:
#                 # Calculate number of stops
#                 number_of_stops = len(segments) - 1
                
#                 # Get transit airports
#                 transit_airports = []
#                 if number_of_stops > 0:
#                     for i, segment in enumerate(segments):
#                         if i < len(segments) - 1:
#                             transit_airports.append(segment['arrival']['iataCode'])
                
#                 transit_airports_str = ','.join(transit_airports) if transit_airports else None
                
#                 flight_price = FlightPrice(
#                     search_id=search.id,
#                     airline=segments[0].get('carrierCode', ''),
#                     flight_number=segments[0].get('number', ''),
#                     price=float(offer.get('price', {}).get('total', 0)),
#                     currency=offer.get('price', {}).get('currency', 'CAD'),
#                     fare_type=offer.get('pricingOptions', {}).get('fareType', ['PUBLISHED'])[0] if offer.get('pricingOptions', {}).get('fareType') else 'PUBLISHED',
#                     duration=itinerary.get('duration', ''),
#                     number_of_stops=number_of_stops,           # NEW
#                     transit_airports=transit_airports_str      # NEW
#                 )
#                 db.add(flight_price)
        
#         db.commit()
#         print(f"✅ Saved search {search.id} with {len(offers)} flight offers!")
#         return search.id
        
#     except Exception as e:
#         db.rollback()
#         print(f"❌ Error saving to database: {e}")
#         import traceback
#         traceback.print_exc()
#     finally:
#         db.close()

def search_flights(origin, destination, date, adults=1, max_results=5):
    # tạo object client (tự động tạo token)
    client = AmadeusClient()
    
    # các argument để search
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "currencyCode": "CAD",
        "max": max_results
    }
    
    # gọi API search flight dến Amadeus
    data = client.get("/v2/shopping/flight-offers", params=params)
    offers = data.get("data", [])
    
    # trả về list
    published_offers = [
        o for o in offers if is_published_fare(o)
    ]
    
    # Save to database
    if published_offers:
        save_flight_data(origin, destination, date, adults, published_offers)
    
    return published_offers  # trả về list, không còn là json