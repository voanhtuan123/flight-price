from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base

class FlightSearch(Base):
    __tablename__ = "flight_searches"
    
    id = Column(Integer, primary_key=True)
    # origin = Column(String, index=True)
    # destination = Column(String, index=True)
    # departure_date = Column(Date)
    # adults = Column(Integer)
    # searched_at = Column(DateTime(timezone=True), server_default=func.now())
    flight_path = Column(String, index=True)
    code_flights = Column(String, index=True)
    flight_date = Column(Date)
    crawl_date = Column(DateTime(timezone=True), server_default=func.now())
    duration = Column(String)
    price = Column(Float)
    stops = Column(Integer)


class FlightAnalyze (Base):
    __tablename__ = "flight_analyzes"
    
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey("flight_searches.id"))
    
    flight_date = Column(Date)
    crawl_date = Column(DateTime(timezone=True), server_default=func.now())
    date_from_crawl_until_departure = Column(Integer)
    duration = Column(String)
    price = Column(Float)
    price_difference_from_last_crawl = Column(Float)