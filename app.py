from fastapi import FastAPI
from pydantic import BaseModel
import csv
import os
import requests

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
        response = requests.post(
    "https://api.resend.com/emails",
    headers={
        "Authorization": f"Bearer {os.getenv('RESEND_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={
        "from": "onboarding@resend.dev",
        "to": RECEIVER_EMAIL,
        "subject": "New Lead Received",
        "html": f"""
        <h2>New Lead Submitted</h2>
        <p><strong>Name:</strong> {data.name}</p>
        <p><strong>Email:</strong> {data.email}</p>
        """
    }
)

print(response.text)

        return {"status": "success"}

    except Exception as e:
        print("Error:", str(e))
        return {"status": "error", "message": str(e)}