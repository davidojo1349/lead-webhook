from fastapi import FastAPI
from pydantic import BaseModel
import csv
import os
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# -----------------------------
# Homepage route
# -----------------------------
@app.get("/")
def home():
    return {"message": "Webhook server is running!"}

# -----------------------------
# Data structure
# -----------------------------
class LeadData(BaseModel):
    name: str
    email: str

# -----------------------------
# CSV file
# -----------------------------
FILE_NAME = "leads.csv"

# -----------------------------
# Email settings
# -----------------------------
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# -----------------------------
# Webhook endpoint
# -----------------------------
@app.post("/webhook")
def webhook(data: LeadData):

    try:

        # -----------------------------
        # Save to CSV
        # -----------------------------
        file_exists = os.path.isfile(FILE_NAME)

        with open(FILE_NAME, mode="a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Name", "Email"])

            writer.writerow([data.name, data.email])

        print(f"Saved: {data.name}, {data.email}")

        # -----------------------------
        # Send email
        # -----------------------------
        subject = "New Lead Received"

        body = f"""
New lead submitted:

Name: {data.name}
Email: {data.email}
"""

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print("Email sent!")

        return {"status": "success"}

    except Exception as e:
        print("Error:", str(e))
        return {"status": "error", "message": str(e)}