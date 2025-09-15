import os
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv("email.env")

SENDER_EMAIL = os.getenv("SMTP_USER")
SENDER_PASSWORD = os.getenv("SMTP_PASS")

CSV_FILE = "student.csv"

df = pd.read_csv(CSV_FILE)
today = datetime.today().date()

for _, row in df.iterrows():
    name = row["name"]
    email = row["email"]
    deadline = datetime.strptime(row["deadline"], "%Y-%m-%d").date()

    if deadline - today == timedelta(days=3):
        subject = "⏳ Reminder: Work due in 3 days"
        body = f"Hello {name},\n\nThis is a reminder that your work is due on {deadline}.\n\nBest regards."

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        print(f"✅ Email sent to {name} ({email})")
