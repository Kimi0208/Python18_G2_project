import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from crm.settings import EMAIL_USER, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER


def send_email_notification(subject, message, to_email):
    msg = MIMEMultipart()

    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)