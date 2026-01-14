"""
Booking Links Generator
Tạo redirect links đến airline websites hoặc OTAs để user tự book vé
"""

from typing import Dict, Optional
from urllib.parse import urlencode


class BookingLinkGenerator:
    """
    Class để generate booking links cho flight offers
    Dễ dàng thêm airlines mới hoặc affiliate programs
    """
    
    def __init__(self, affiliate_id: Optional[str] = None):
        """
        Args:
            affiliate_id: ID cho affiliate programs (nếu có)
        """
        self.affiliate_id = affiliate_id
        
        # Airline deep link templates
        self.airline_templates = {
            "AC": "https://www.aircanada.com/en/search",
            "WS": "https://www.westjet.com/en-ca/book-trip/flight",
            "UA": "https://www.united.com/en/us/fsr/choose-flights",
            "AA": "https://www.aa.com/booking/find-flights",
            "DL": "https://www.delta.com/flight-search/book-a-flight",
            "AS": "https://www.alaskaair.com/booking/reservation/search",
            "VN": "https://www.vietnamairlines.com/en/book-a-flight",
            "BA": "https://www.britishairways.com/travel/book/public/en_ca",
            "LH": "https://www.lufthansa.com/ca/en/booking",
            "AF": "https://www.airfrance.ca/en/booking",
            "KL": "https://www.klm.com/search",
            "NH": "https://www.ana.co.jp/en/ca/book-plan/",
            "SQ": "https://www.singaporeair.com/en_UK/ca/plan-travel/book/",
        }
    
    def get_booking_url(self, offer: Dict, strategy: str = "auto") -> str:
        """
        Generate booking URL for a flight offer
        
        Args:
            offer: Flight offer từ Amadeus API
            strategy: "airline" | "google" | "affiliate" | "auto"
            
        Returns:
            Booking URL string
        """
        try:
            # Extract flight info
            carrier = offer["validatingAirlineCodes"][0]
            segments = offer["itineraries"][0]["segments"]
            origin = segments[0]["departure"]["iataCode"]
            destination = segments[-1]["arrival"]["iataCode"]
            dep_date = segments[0]["departure"]["at"][:10]
            
            # Return date nếu có (round trip)
            return_date = None
            if len(offer.get("itineraries", [])) > 1:
                return_segments = offer["itineraries"][1]["segments"]
                return_date = return_segments[0]["departure"]["at"][:10]
            
            # 🔧 FIX: Default to Google Flights (most reliable)
            if strategy == "auto":
                # Google Flights luôn work, airline links hay fail
                return self._build_google_flights_url(origin, destination, dep_date, return_date)
            
            elif strategy == "airline":
                # Thử airline trước, fallback Google nếu không có
                if carrier in self.airline_templates:
                    return self._build_airline_url(carrier, origin, destination, dep_date, return_date)
                else:
                    return self._build_google_flights_url(origin, destination, dep_date, return_date)
            
            elif strategy == "google":
                return self._build_google_flights_url(origin, destination, dep_date, return_date)
            
            elif strategy == "affiliate":
                return self._build_affiliate_url(origin, destination, dep_date, return_date)
            
            else:
                return self._build_google_flights_url(origin, destination, dep_date, return_date)
        
        except Exception as e:
            print(f"⚠️ Error generating booking URL: {e}")
            return "https://www.google.com/flights"
    
    def _build_airline_url(self, carrier: str, origin: str, destination: str, 
                          dep_date: str, return_date: Optional[str] = None) -> str:
        """Build deep link to airline website"""
        
        base_url = self.airline_templates.get(carrier)
        if not base_url:
            # Airline không support → fallback Google Flights
            return self._build_google_flights_url(origin, destination, dep_date, return_date)
        
        # 🔧 FIX: Nếu airline URL không work, dễ debug
        try:
            # Parameters cho từng airline (mỗi airline có format khác nhau)
            if carrier == "AC":  # Air Canada
                params = {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": dep_date,
                    "adults": 1,
                }
                if return_date:
                    params["returnDate"] = return_date
            
            elif carrier == "WS":  # WestJet
                params = {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": dep_date,
                }
            
            elif carrier == "UA":  # United
                params = {
                    "f": origin,
                    "t": destination,
                    "d": dep_date,
                    "tt": "1" if not return_date else "2",
                    "at": "1",
                }
                if return_date:
                    params["r"] = return_date
            
            elif carrier == "AA":  # American Airlines
                params = {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": dep_date,
                    "adults": 1,
                }
                if return_date:
                    params["returnDate"] = return_date
            
            elif carrier == "VN":  # Vietnam Airlines
                trip_type = "roundtrip" if return_date else "oneway"
                params = {
                    "trip": trip_type,
                    "from": origin,
                    "to": destination,
                    "date": dep_date,
                }
                if return_date:
                    params["returnDate"] = return_date
            
            else:
                # Generic format (might not work)
                params = {
                    "from": origin,
                    "to": destination,
                    "departure": dep_date,
                }
            
            url = f"{base_url}?{urlencode(params)}"
            
            # 🔧 ADD: Thêm note để user biết link có thể không work
            # (Trả về tuple nếu muốn thêm warning)
            return url
            
        except Exception as e:
            # Nếu có lỗi → fallback Google Flights
            print(f"⚠️ Error building {carrier} URL: {e}, using Google Flights")
            return self._build_google_flights_url(origin, destination, dep_date, return_date)
    
    def _build_google_flights_url(self, origin: str, destination: str, 
                                  dep_date: str, return_date: Optional[str] = None) -> str:
        """Build Google Flights URL"""
        
        # Format date: YYYY-MM-DD → YYYYMMDD
        dep_formatted = dep_date.replace("-", "")
        
        if return_date:
            ret_formatted = return_date.replace("-", "")
            flight_string = f"{origin}.{destination}.{dep_formatted}*{destination}.{origin}.{ret_formatted}"
        else:
            flight_string = f"{origin}.{destination}.{dep_formatted}"
        
        return f"https://www.google.com/flights?hl=en#flt={flight_string};c:CAD"
    
    def _build_affiliate_url(self, origin: str, destination: str, 
                            dep_date: str, return_date: Optional[str] = None) -> str:
        """
        Build affiliate URL (Skyscanner, Expedia, etc.)
        Cần có affiliate_id để kiếm commission
        """
        
        if not self.affiliate_id:
            print("⚠️ No affiliate ID set, using Google Flights")
            return self._build_google_flights_url(origin, destination, dep_date, return_date)
        
        # Example: Skyscanner affiliate
        dep_formatted = dep_date.replace("-", "")
        ret_formatted = return_date.replace("-", "") if return_date else ""
        
        if return_date:
            url = (
                f"https://www.skyscanner.com/transport/flights/"
                f"{origin}/{destination}/{dep_formatted}/{ret_formatted}/"
                f"?associateid={self.affiliate_id}"
            )
        else:
            url = (
                f"https://www.skyscanner.com/transport/flights/"
                f"{origin}/{destination}/{dep_formatted}/"
                f"?associateid={self.affiliate_id}"
            )
        
        return url
    
    def get_multiple_booking_options(self, offer: Dict) -> Dict[str, str]:
        """
        Get multiple booking options cho user
        
        Returns:
            Dict với keys: "airline", "google", "affiliate"
        """
        return {
            "airline": self.get_booking_url(offer, strategy="airline"),
            "google": self.get_booking_url(offer, strategy="google"),
            "affiliate": self.get_booking_url(offer, strategy="affiliate"),
        }
    
    def add_airline(self, carrier_code: str, base_url: str):
        """
        Thêm airline mới vào hệ thống
        
        Args:
            carrier_code: 2-letter IATA code (e.g., "AC")
            base_url: Base URL của airline booking page
        """
        self.airline_templates[carrier_code] = base_url
        print(f"✅ Added {carrier_code}: {base_url}")


# ============================================================================
# HELPER FUNCTIONS (để dùng đơn giản hơn)
# ============================================================================

def get_booking_link(offer: Dict, strategy: str = "auto") -> str:
    """
    Quick helper function để generate booking link
    
    Usage:
        url = get_booking_link(offer)
        url = get_booking_link(offer, strategy="google")
    """
    generator = BookingLinkGenerator()
    return generator.get_booking_url(offer, strategy)


def get_all_booking_options(offer: Dict) -> Dict[str, str]:
    """
    Get tất cả booking options
    
    Returns:
        {
            "airline": "https://...",
            "google": "https://...",
            "affiliate": "https://..."
        }
    """
    generator = BookingLinkGenerator()
    return generator.get_multiple_booking_options(offer)