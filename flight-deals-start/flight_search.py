import os
import requests
import datetime
from flight_data import FlightData


Tequila_API_KEY = os.environ["Tequila_API_KEY"]
FLY_FROM = "LON"
today = datetime
tequila_headers = {
            "apikey": Tequila_API_KEY
}


class FlightSearch:

    def get_destination_iata(self, city_name):
        tequila_endpoint_location = "https://api.tequila.kiwi.com/"
        query = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(
            url=f"{tequila_endpoint_location}locations/query",
            headers=tequila_headers,
            params=query
        )
        response.raise_for_status()
        response_data = response.json()
        iata = response_data["locations"][0]["code"]
        return iata

    def search(self, departure_airport, destination_airport, outbound_date, inbound_date):
        tequila_endpoint_search = "https://api.tequila.kiwi.com/v2"
        query = {
            "fly_from": departure_airport,
            "fly_to": destination_airport,
            "date_from": outbound_date,
            "date_to": inbound_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=f"{tequila_endpoint_search}/search", params=query, headers=tequila_headers)
        try:
            search_response = response.json()["data"][0]
            print(search_response)
        except IndexError:
            query["max_stopovers"] = 2
            response = requests.get(url=f"{tequila_endpoint_search}/search", params=query, headers=tequila_headers)
            try:
                data = response.json()["data"][0]
                print(data)
            except IndexError:
                query["max_stopovers"] = 4
                response = requests.get(url=f"{tequila_endpoint_search}/search", params=query, headers=tequila_headers)
                try:
                    data = response.json()["data"][0]
                    print(data)
                except IndexError:
                    print("No data for this flight")
                    return None
                else:
                    data = response.json()["data"][0]
                    print(data)
                    flight_data = FlightData(
                        price=data["price"],
                        departure_city=data["route"][0]["cityFrom"],
                        departure_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][1]["cityTo"],
                        destination_airport=data["route"][1]["flyTo"],
                        outbound_date=data["route"][0]["local_departure"].split("T")[0],
                        inbound_date=data["route"][2]["local_departure"].split("T")[0],
                        stop_overs=2,
                        via_city=data["route"][0]["cityTo"]
                    )
                    return flight_data

            else:
                flight_data = FlightData(
                    price=data["price"],
                    departure_city=data["route"][0]["cityFrom"],
                    departure_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    outbound_date=data["route"][0]["local_departure"].split("T")[0],
                    inbound_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data

        else:
            flight_data = FlightData(
                price=search_response["price"],
                departure_city=search_response["route"][0]["cityFrom"],
                departure_airport=search_response["route"][0]["flyFrom"],
                destination_city=search_response["route"][0]["cityTo"],
                destination_airport=search_response["route"][0]["flyTo"],
                outbound_date=search_response["route"][0]["local_departure"].split("T")[0],
                inbound_date=search_response["route"][1]["local_departure"].split("T")[0]
            )
            return flight_data
