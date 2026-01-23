from twilio.rest import Client

def send_whatsapp(msg):
    client = Client("SID", "TOKEN")
    client.messages.create(
        from_="whatsapp:+14155238886",
        to="whatsapp:+91XXXXXXXXXX",
        body=msg
    )

