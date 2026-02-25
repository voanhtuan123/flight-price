from app.db.database import SessionLocal, Base, engine
from app.db.table_models import FlightSearch
from app.flight_search import search_flights
from datetime import datetime, timedelta

#Initialize database
print("Initializing database...")
Base.metadata.create_all(bind=engine)

#params
origin = "YYC"
destination = "HAN"
start_date = datetime.strptime("2026-04-15", "%Y-%m-%d")
end_date = datetime.strptime("2026-06-30", "%Y-%m-%d")
max = 10
crawl_date = datetime.now().strftime("%Y-%m-%d")

#Process flight data
all_flights = []

while start_date <= end_date:
    date = start_date.strftime("%Y-%m-%d")
    print(f"\nCrawling date: {date}")
    

    #Call API to search flights
    print(f"Searching flights from {origin} to {destination} on {date}...")
    data = search_flights(
        origin=origin,
        destination=destination,
        date=date,
        max_results=max
    )


    for offer in data:
        # Get price
        price = offer["price"]["total"]
        print(f"Price: {price} ")

        # Get duration
        flight_time = offer["itineraries"][0]["duration"]
        print("Duration: ", flight_time)
        
        # Get flight path and codes
        airports = [origin]
        flight_code = []
        segment = offer["itineraries"][0]["segments"]
        for i in range(len(segment)):
            airports.append(segment[i]['arrival']['iataCode'])
            flight_code.append(f"{segment[i]['carrierCode']}{segment[i]['number']}")

        flights = " - ".join(airports)
        print("Flights: ", flights)
        
        code_flights = " - ".join(flight_code)
        print("Flight code: ", code_flights)
        print("-----")

        # Save flight data to dictionary
        flight_data = {
            "duration": flight_time,
            "flights_path": flights,
            "code_flights": code_flights,
            "price": price,
            "departure_date": date,
            "crawl_date": crawl_date,
            "stops": len(airports) - 2
        }
        # Append to all flights list
        all_flights.append(flight_data)
        
    # Move to next date
    start_date += timedelta(days=1)

print("\nAll Flights Data:", all_flights)

print(f"\n Saving {len(all_flights)} flights to database...")
db = SessionLocal()
try:
    for flight in all_flights:
        flight_record = FlightSearch(
            flight_path=flight["flights_path"],
            code_flights=flight["code_flights"],
            flight_date=flight["departure_date"],
            crawl_date=flight["crawl_date"],
            duration=flight["duration"],
            price=float(flight["price"]),
            stops=flight["stops"]
        )
        db.add(flight_record)
    
    db.commit()
    print("All flights saved to database!")
    
except Exception as e:
    db.rollback()
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
