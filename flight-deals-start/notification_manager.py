import os
import smtplib
from twilio.rest import Client

twilio_account_sid = os.environ["twilio_account_sid"]
twilio_auth_token = os.environ["twilio_auth_token"]
twilio_phone_number = os.environ["twilio_phone_number"]
guest_phone_number = os.environ["guest_phone_number"]
smtp_my_email = os.environ["smtp_my_email"]
smtp_my_password = os.environ["smtp_my_password"]


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(twilio_account_sid, twilio_auth_token)

    pass

    def send_sms(self, price, departure_city, departure_airport, arrival_city, arrival_airport, outbound_date,
                 inbound_date):
        message = self.client.messages \
            .create(
                body=f"Look at this!👀 Only £{price} to fly from {departure_city}-{departure_airport} to {arrival_city}-{arrival_airport} from {outbound_date} to {inbound_date}!🛫",
                from_=twilio_phone_number,
                to=guest_phone_number
            )
        print(message.sid)

    def send_emails(self, emails, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(smtp_my_email, smtp_my_password)
            for email in emails:
                connection.sendmail(
                    from_addr=smtp_my_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                )