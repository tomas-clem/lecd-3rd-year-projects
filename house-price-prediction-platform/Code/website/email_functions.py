import smtplib
import db
from email.message import EmailMessage


import smtplib, ssl

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
server.login("prevemoscasas@gmail.com", "{password}") # Mudar para guardar em outro lado
sender_email = "prevemoscasas@gmail.com"


def recover_email(email,name,code):
    with open("./email_templates/recover.txt","r") as f:
        server.login("prevemoscasas@gmail.com", "{password}") # Mudar para guardar em outro lado
        sender_email = "prevemoscasas@gmail.com"
        message = f.read().format(name=name,code=code).encode('utf-8')
        server.sendmail(sender_email, email, message)
        server.quit()


