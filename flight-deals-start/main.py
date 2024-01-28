import data_manager
import flight_search
import notification_manager
import datetime

departure_city_iata = "LON"

sheet = data_manager.DataManager()
flight_query = flight_search.FlightSearch()
messenger = notification_manager.NotificationManager()


sheet_data = sheet.get_data()

if sheet_data[0]["iataCode"] == "":
    cities = [row["city"] for row in sheet_data]
    sheet.city_does = flight_query.get_destination_iata(cities)
    sheet.update_destination_iata()
    sheet_data = sheet.get_data()

sheet_destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
six_month = datetime.datetime.now() + datetime.timedelta(days=6 * 30)
tomorrow_date = tomorrow.date()
six_month_date = six_month.date()

for destination_code in sheet_destinations:
    flight = flight_query.search(
        departure_airport=departure_city_iata,
        destination_airport=destination_code,
        outbound_date=tomorrow_date,
        inbound_date=six_month_date
    )
    print(flight.price)
    if flight is None:
        continue

    if flight.price < sheet_destinations[destination_code]["price"]:

        users = sheet.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only £{flight.price} to fly from {flight.departure_city}-{flight.departure_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.outbound_date} to {flight.inbound_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        messenger.send_email(emails, message)
