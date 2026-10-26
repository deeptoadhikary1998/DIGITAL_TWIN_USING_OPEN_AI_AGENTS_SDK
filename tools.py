import os
import requests
from dotenv import load_dotenv
from agents import function_tool
from send_email import send_email

load_dotenv(override=True)

# Pushover credetials 
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

# Email credentials 
from_email = os.getenv("EMAIL_ADDRESS")



def push(text):
    requests.post(
        pushover_url,
        data={
            "token": pushover_token,
            "user": pushover_user,
            "message": text,
        },
    )


@function_tool
def collect_emails(emails: list[str], name: str = "there") -> str:
    """
    Collect email addresses explicitly requested by the user.

    The agent should extract every unique email address
    from the user's prompt and provide them in emails.
    Remove duplicates before calling this function.
    Extract the person's name if available; otherwise,
    use 'there'.

    Send a confirmation email to each address and send
    a push notification summarizing the operation.
    """
    sent = 0

    for email in emails:
        try:
            send_email(
                to_email=email,
                subject="Email Confirmation",
                body=f"Hello {name}, your email was recorded. Please reply to this email to continue the conversation.",
            )
            sent += 1
        except Exception as e:
            print(f"Email error: {e}")

    push(f"Collected {len(emails)} addresses. Sent {sent} emails.")

    return f"Collected {len(emails)} addresses; sent {sent} confirmations."




@function_tool
def note_unknown_questions(question: str) -> str:
    """Notify the admin about an unanswered question by push and email."""

    notification = f"Question I could not answer: {question}"

    try:
        push(notification)
    except Exception as e:
        print(f"Pushover error: {e}")

    try:
        send_email(
            to_email=from_email,
            subject="Unanswered Question",
            body=notification,
          )
    except Exception as e:
        print(f"Email sending failed: {type(e).__name__}: {e}")
        return "The push notification was attempted, but the admin email failed."

    return "The unanswered question was sent to the admin by email."


@function_tool
def note_unknown_questions_ooc(question: str) -> str:
    """Notify the admin about any personal question or any question that is out of context via push and email."""

    notification = f"Question I could not answer OOC category: {question}"

    try:
        push(notification)
    except Exception as e:
        print(f"Pushover error: {e}")

    try:
        send_email(
            to_email=from_email,
            subject="Unanswered Question OOC category",
            body=notification,
          )
    except Exception as e:
        print(f"Email sending failed: {type(e).__name__}: {e}")
        return "The push notification was attempted, but the admin email failed."

    return "The unanswered question was sent to the admin by email."