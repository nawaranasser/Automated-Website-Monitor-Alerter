# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def send_alert_email(alert_subject, alert_message):
    """
    Sends an email alert using Gmail SMTP
    """
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = config.GMAIL_SENDER
        msg['To'] = config.RECIPIENT_EMAIL
        msg['Subject'] = alert_subject

        # Add the alert message to the email body
        msg.attach(MIMEText(alert_message, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        # Login with app password
        server.login(config.GMAIL_SENDER, config.GMAIL_APP_PASSWORD)
        # Send email
        text = msg.as_string()
        server.sendmail(config.GMAIL_SENDER, config.RECIPIENT_EMAIL, text)
        server.quit()
        
        print(f"📧 Email alert sent successfully to {config.RECIPIENT_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False