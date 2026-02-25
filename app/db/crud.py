from sqlalchemy.orm import Session
from . import table_models
from datetime import datetime

def create_flight_search(db: Session, origin: str, destination: str, 
                        departure_date: str, adults: int):
    """Create a flight search record"""
    search = table_models.FlightSearch(
        origin=origin,
        destination=destination,
        departure_date=datetime.strptime(departure_date, "%Y-%m-%d").date(),
        adults=adults
    )
    db.add(search)
    db.flush()
    return search

def create_flight_price(db: Session, search_id: int, airline: str, 
                       flight_number: str, price: float, currency: str,
                       fare_type: str, duration: str):
    """Create a flight price record"""
    flight_price = table_models.FlightAnalyze(
        search_id=search_id,
        airline=airline,
        flight_number=flight_number,
        price=price,
        currency=currency,
        fare_type=fare_type,
        duration=duration
    )
    db.add(flight_price)
    return flight_price