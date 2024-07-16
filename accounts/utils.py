from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.conf import settings

def send_email(subject, body, sender, recipients, password):
    print("Sending email...")
    print("Recipient: ", recipients)
    print("Subject: ", subject)
    print("Sender: ", sender)
    print("Password: ", password)
    
    try:
        # Create a MIMEText object for HTML
        msg = MIMEMultipart("alternative")
        html_body = MIMEText(body, "html")
        msg.attach(html_body)

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

        print("Email sent successfully!")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
