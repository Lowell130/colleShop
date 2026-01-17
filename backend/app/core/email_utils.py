import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_email_background(to_email: str, subject: str, html_content: str):
    """
    Sends an email in the background (synchronous function run in thread by FastAPI).
    """
    if not settings.SENDER_EMAIL or not settings.SENDER_PASSWORD:
        print("Email configuration missing. Skipping email send.")
        return

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.SENDER_EMAIL
        message["To"] = to_email

        # HTML body
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        # Connect to SMTP Server
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
            server.sendmail(settings.SENDER_EMAIL, to_email, message.as_string())
            
        print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
