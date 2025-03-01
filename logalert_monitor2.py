import time
import smtplib
import time
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOG_FILE_PATH = "app.log"  # Change this to your actual log file

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP Server
SMTP_PORT = 587
SENDER_EMAIL = "bismiba7@gmail.com"  # Replace with your email
SENDER_PASSWORD = "niezmtoxwehrguoe"  # Use App Password, NOT your actual password
RECEIVER_EMAIL = "bismiba166@gmail.com"  # Replace with recipient email

def send_email(subject, body):
    """Send an email alert."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Establish connection with SMTP server
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)  # Secure connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print("✅ Email alert sent!")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def monitor_log():
    """Monitor log file for errors and send email alerts."""
    with open(LOG_FILE_PATH, "r") as file:
        file.seek(0, 2)  # Move to the end of the file

        while True:
            line = file.readline()
            if not line:
                time.sleep(1)  # Wait for new log entries
                continue

            if "ERROR" in line or "WARNING" in line:
                print(f"🚨 ALERT: {line.strip()}")
                send_email("Log Alert 🚨", f"An error was detected:\n\n{line.strip()}")

if __name__ == "__main__":
    print("Monitoring log file for errors and warnings...")
    monitor_log()