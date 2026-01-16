from app.flight_search import search_flights
from datetime import datetime

origin = "YYC"
destination = "HAN"
date = "2026-03-15"
max = 10
crawl_date = datetime.now().strftime("%Y-%m-%d")

data = search_flights(
    origin=origin,
    destination=destination,
    date=date,
    max_results=max
)

all_flights = []

for offer in data:
    
    price = offer["price"]["total"]
    print(f"Price: {price} ")

    flight_time = offer["itineraries"][0]["duration"]
    print("Duration: ", flight_time)
    
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

    flight_data = {
        "duration": flight_time,
        "flights_path": flights,
        "code_flights": code_flights,
        "price": price,
        "departure_date": date,
        "crawl_date": crawl_date,
        "stops": len(airports) - 2
    }

    all_flights.append(flight_data)

print("\nAll Flights Data:", all_flights)