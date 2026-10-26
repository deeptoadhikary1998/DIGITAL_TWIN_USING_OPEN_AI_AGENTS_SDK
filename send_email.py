
import base64
import os
from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]



import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def load_credentials():
    token_path = os.environ.get(
        "GOOGLE_TOKEN_FILE",
        "token.json"
    )

    credentials = Credentials.from_authorized_user_file(
        token_path,
        SCOPES
    )

    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            raise RuntimeError(
                "Credentials invalid. Reauthorization is needed."
            )

    return credentials

    

def send_email(to_email, subject, body):
    credentials = load_credentials()

    gmail = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    message = EmailMessage()
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    result = gmail.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()

    print("Email accepted by Gmail API.")
    print("Message ID:", result["id"])


if __name__ == "__main__":
    send_email(
        to_email="deeptoadhikary1998@gmail.com",
        subject="Testing Gmail API",
        body="Hello! This email was sent using Deepto's twin chat bot it's a test."
    )
