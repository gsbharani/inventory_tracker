import smtplib
from email.mime.text import MIMEText

def send_email(msg):
    sender = "yourmail@gmail.com"
    password = "gmail_app_password"
    receiver = "vendor@gmail.com"

    message = MIMEText(msg)
    message["Subject"] = "Inventory Alert"
    message["From"] = sender
    message["To"] = receiver

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.send_message(message)
    server.quit()
