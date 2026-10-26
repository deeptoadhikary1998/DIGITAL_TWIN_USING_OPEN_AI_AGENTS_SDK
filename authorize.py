import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        "/etc/secrets/credentials.json",
        SCOPES
    )

    credentials = flow.run_local_server(
        port=0,
        access_type="offline",
        prompt="consent"
    )

    Path("token.json").write_text(
        credentials.to_json(),
        encoding="utf-8"
    )

    print("Authorization successful!")
    print("token.json has been created.")

if __name__ == "__main__":
    main()
