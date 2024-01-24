import os
import requests

sheety_endpoint_prices = os.environ["sheety_endpoint_prices"]
sheety_endpoint_users = os.environ["sheety_endpoint_users"]
APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
sheety_bearer = os.environ["sheety_bearer"]
sheety_headers = {
    "Authorization": f"Bearer {sheety_bearer}"
}


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_data(self):
        response = requests.get(url=sheety_endpoint_prices, headers=sheety_headers).json()
        self.destination_data = response["prices"]
        return self.destination_data

    def update_destination_iata(self):
        for city in self.destination_data:
            new_iata = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{sheety_endpoint_prices}/{city["id"]}",
                json=new_iata,
                headers=sheety_headers
            )
            print(response.text)

    def get_customer_emails(self):
        customers_endpoint = sheety_endpoint_users
        response = requests.get(url=customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
