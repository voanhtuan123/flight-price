from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base

class FlightSearch(Base):
    __tablename__ = "flight_searches"
    
    id = Column(Integer, primary_key=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    departure_date = Column(Date)
    adults = Column(Integer)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())

class FlightPrice(Base):
    __tablename__ = "flight_prices"
    
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey("flight_searches.id"))
    airline = Column(String)
    flight_number = Column(String)
    price = Column(Float)
    currency = Column(String)
    fare_type = Column(String)
    duration = Column(String)
    number_of_stops = Column(Integer)      
    transit_airports = Column(Text)        
    checked_at = Column(DateTime(timezone=True), server_default=func.now())