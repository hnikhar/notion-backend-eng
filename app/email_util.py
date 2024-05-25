import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings

def send_email(subject: str, recipients: list, body: str):
    msg = MIMEMultipart()
    msg['From'] = settings.MAIL_FROM
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM, recipients, msg.as_string())

def queue_email_to_prospect(email: str):
    subject = "New Lead Submission"
    body = "Thank you for your submission."
    send_email(subject, [email], body)

def queue_email_to_attorney():
    subject = "New Lead Submission"
    body = "A new lead has been submitted."
    send_email(subject, ["attorney@example.com"], body)
