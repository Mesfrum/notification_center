from main import read_email_address
from main import send_email

toEmails = read_email_address()
print(toEmails)

body = "You have subscribed to notification serveice for sakec placement portal. Please mark this email address as not spam."
subject = "Notification service for sakec placement portal"


send_email(subject,body,toEmails,"NIL")
