import requests
import os

def send_email(to, subject, body):
    requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {os.getenv('RESEND_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "from": "Website Bot <onboarding@resend.dev>",
            "to": [to],
            "subject": subject,
            "text": body,
        },
    )
