import psutil
import os
import smtplib
from email.mime.text import MIMEText
import time

# Email Configuration (Replace with your details)
SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587  
EMAIL_SENDER = "bismiba7@gmail.com"  
EMAIL_PASSWORD = "gqzhpcwficujzmlr"  
EMAIL_RECEIVER = "bismiba166@gmail.com"  

# Function to send an email alert
def send_email_alert(cpu_usage):
    try:
        subject = "⚠️ High CPU Usage Alert!"
        body = f"Warning! Your system's CPU usage has reached {cpu_usage}%."
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        
        print("✅ Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Function to terminate high-CPU non-system processes
def take_action():
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if process.info['cpu_percent'] > 80:  # Change the threshold if needed
            process_name = process.info['name']
            pid = process.info['pid']

            # List of system processes to exclude
            critical_processes = [
                "csrss.exe", "winlogon.exe", "smss.exe", "services.exe", 
                "lsass.exe", "explorer.exe", "svchost.exe", "taskmgr.exe"
            ]

            if process_name.lower() in critical_processes:
                print(f"⚠️ Skipping critical process: {process_name} (PID: {pid})")
                continue  # Do not attempt to kill

            try:
                print(f"🛑 Terminating process: {process_name} (PID: {pid})")
                os.kill(pid, 9)
            except PermissionError:
                print(f"❌ Failed to terminate {process_name}: Permission denied")
            except Exception as e:
                print(f"❌ Error terminating {process_name}: {e}")

# Function to check CPU usage
def check_cpu_usage():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"CPU Usage: {cpu_usage}%")
        
        if cpu_usage > 90:  # Change the threshold if needed
            print("⚠️ Warning! High CPU usage detected!")
            send_email_alert(cpu_usage)
            print("🛠 Taking action to reduce CPU usage...")
            take_action()
        
        time.sleep(5)  # Adjust monitoring frequency

# Start monitoring
if __name__ == "__main__":
    print("🚀 System Health Monitoring Started...")
    check_cpu_usage()