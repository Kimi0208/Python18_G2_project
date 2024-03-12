import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_notification(subject, message, from_email, to_email, smtp_server, smtp_port, smtp_username, smtp_password):
    msg = MIMEMultipart()

    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

#
# ttt = 'CRM:  '
#
# subject = ttt + "Тема"
# message = "Тело письма"
# from_email = "dkan@elcat.kg"
# to_email = "кому"
# smtp_server = "сервер"
# smtp_port = 465
# smtp_username = 'логин'
# smtp_password = "пароль"
#
# try:
#     send_email_notification(subject, message, from_email, to_email, smtp_server, smtp_port, smtp_username, smtp_password)
# except Exception as e:
#     print("Произошла ошибка при отправке email:", e)