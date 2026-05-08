import smtplib
from email.mime.text import MIMEText

from app.core.config import settings


def send_order_email(to_email: str, order_code: str):
    body = f'Your Little Wok Story order {order_code} has been placed and is being prepared.'

    if not settings.smtp_host:
        # local/dev fallback
        print(f'[Email simulation] to={to_email}: {body}')
        return

    msg = MIMEText(body)
    msg['Subject'] = f'Order Confirmation - {order_code}'
    msg['From'] = settings.mail_from
    msg['To'] = to_email

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.mail_from, [to_email], msg.as_string())
