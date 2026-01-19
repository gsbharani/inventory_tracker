from twilio.rest import Client

def send_whatsapp(msg):
    client = Client("TWILIO_SID", "TWILIO_AUTH")
    client.messages.create(
        body=msg,
        from_="whatsapp:+14155238886",
        to="whatsapp:+91XXXXXXXXXX"
    )
