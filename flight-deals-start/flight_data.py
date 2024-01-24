class FlightData:
    def __init__(self, price, departure_city, departure_airport, destination_city, destination_airport, outbound_date, inbound_date, stop_overs=0, via_city=""):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        self.stop_overs = stop_overs
        self.via_city = via_city

