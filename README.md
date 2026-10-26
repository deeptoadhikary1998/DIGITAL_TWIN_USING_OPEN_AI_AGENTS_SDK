# Meet Deepto \| AI Digital Twin

An interactive AI-powered digital twin that lets visitors explore
Deepto's professional background, ask career-related questions, and find
ways to get in touch.

## Features

-   **Conversational digital twin:** Answers questions about
    professional background, skills, experience, and projects using
    information from the resume, LinkedIn profile, and professional
    summary.
-   **Agentic workflow:** Uses the OpenAI Agents SDK with DeepSeek's
    chat model to respond and call tools when needed.
-   **Contact workflow:** Can collect email addresses when a visitor
    explicitly requests contact or shares an address for follow-up, and
    send confirmation emails.
-   **Unanswered-question notifications:** Sends an email and a Pushover
    notification when the agent cannot answer a question. A separate
    tool handles personal or out-of-context questions.
-   **Gmail API integration:** Sends emails through Google's Gmail API
    using OAuth 2.0.
-   **Pushover notifications:** Sends push notifications for relevant
    contact and unanswered-question events.
-   **Gradio interface:** Provides a browser-based chat UI with custom
    CSS and JavaScript.
-   **Session history:** Uses `SQLiteSession` and a local SQLite
    database to retain conversation history per Gradio session.

## Tech stack

-   Python
-   Gradio
-   OpenAI Agents SDK
-   DeepSeek API (through the OpenAI-compatible client)
-   Google Gmail API and OAuth 2.0
-   Pushover
-   SQLite
-   `pypdf` for extracting text from PDF documents

## Project structure

``` text
.
├── app.py                 # Gradio UI, DeepSeek client, agent and chat handler
├── tools.py               # Contact collection and notification tools
├── send_email.py          # Gmail API email-sending helper
├── authorize.py           # Local Google OAuth authorization flow
├── context.py             # Loads resume/LinkedIn/summary and builds agent context
├── styles.py              # UI examples, CSS and JavaScript
├── requirements.txt       # Python dependencies
├── resources/
│   ├── linkedin.pdf       # LinkedIn/profile export (expected by context.py)
│   ├── resume.pdf         # Resume PDF (expected by context.py)
│   └── summary.txt        # Professional summary (expected by context.py)
├── credentials.json       # Google OAuth client configuration (private; do not commit)
├── token.json             # Google OAuth tokens (private; do not commit)
├── .env                   # Local environment variables (private; do not commit)
└── digital_twin_sessions.db  # SQLite session database (created at runtime)
```

The `resources/` files are expected by `context.py`. Ensure they exist
at those paths, or update the paths in `context.py`.

## Prerequisites

-   Python 3.10 or a compatible version supported by your installed
    dependencies.
-   A DeepSeek API key.
-   Pushover application credentials if push notifications are desired.
-   A Gmail account and Google Cloud project with the Gmail API enabled.
-   OAuth credentials for the Gmail account used to send messages.

## Local setup

### 1. Clone the repository and enter the project directory

``` bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

### 2. Create and activate a virtual environment

Windows PowerShell:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

``` bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local file named `.env` in the same directory as `app.py`. Add
your own values:

``` dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_application_token
PUSHOVER_URL=https://api.pushover.net/1/messages.json

EMAIL_ADDRESS=your_admin_email@example.com
```

Do not paste real credentials into this README, commit them to Git, or
share them in screenshots or logs. The application calls
`load_dotenv(override=True)`, so the local `.env` file can override
environment variables already set in the shell.

### 5. Configure Gmail API OAuth

1.  Open the [Google Cloud Console](https://console.cloud.google.com/).

2.  Create or select a project and enable **Gmail API**.

3.  Configure the Google Auth Platform consent screen and audience/test
    users as appropriate.

4.  Create an OAuth client for local authorization (the provided
    `authorize.py` uses Google's installed-app flow).

5.  Download the client JSON and save it as `credentials.json` in the
    project directory.

6.  Run:

    ``` bash
    python authorize.py
    ```

7.  Sign in to the Gmail account that should send emails and grant the
    requested `gmail.send` permission.

8.  The script creates `token.json`. Keep this file private.

Google OAuth testing-mode refresh tokens for Gmail scopes may expire
after seven days. Review Google's current publishing and verification
requirements for ongoing use.

### 6. Run the application

``` bash
python app.py
```

Open the local URL printed by Gradio in your terminal.

## Deploying to Render

1.  Push the application code to the Git repository connected to Render.

2.  In Render, create or open the Python web service.

3.  Configure the start command, for example:

    ``` bash
    python app.py
    ```

4.  Add the environment variables listed above in the Render service's
    **Environment** settings.

5.  Add `credentials.json` and `token.json` as **Secret Files** if your
    code reads them from the Render secret-file directory. Update
    `send_email.py` to use the corresponding paths (commonly
    `/etc/secrets/credentials.json` and `/etc/secrets/token.json` for a
    non-Docker Render service).

6.  Confirm that the email-sending code uses the deployed secret-file
    path and that OAuth tokens are valid.

7.  Redeploy and check Render logs for startup errors.

**Important:** Render does not automatically have access to files on
your laptop. Do not commit `.env`, `credentials.json`, or `token.json`
to GitHub. The deployed application must explicitly read secrets from
Render's environment or Secret Files.

## Security notes

-   Never commit `.env`, `credentials.json`, or `token.json`.

-   Add these entries to `.gitignore`:

    ``` gitignore
    .env
    env
    credentials.json
    token.json
    venv/
    .venv/
    __pycache__/
    *.db
    ```

-   If a key or token is accidentally exposed, revoke or rotate it
    immediately. Removing it from the latest commit alone does not
    remove it from Git history.

-   Avoid printing API keys, OAuth tokens, or full secret contents in
    logs.

-   Request only the Gmail permissions the application needs.

-   Treat visitor email addresses and conversation content as private
    data.

## How the tools work

-   `collect_emails`: sends a confirmation email to collected addresses
    and sends a Pushover notification summarizing the operation.
-   `note_unknown_questions`: notifies the administrator when the agent
    cannot answer a question.
-   `note_unknown_questions_ooc`: notifies the administrator about
    personal or out-of-context questions.

The agent's instructions determine when these tools should be called.
Test these workflows carefully before making the application publicly
available.

## Troubleshooting

### Missing DeepSeek credentials

-   Confirm `.env` is named exactly `.env`, not `env.txt` or `env`.
-   Confirm it is in the same directory as `app.py`.
-   Confirm `DEEPSEEK_API_KEY` and `DEEPSEEK_BASE_URL` are set.
-   Restart the application after changing environment variables.

### `ImportError` for a tool

-   Confirm the function exists in `tools.py` and its spelling matches
    the import in `app.py`.
-   Commit and push the updated files to the branch Render deploys.
-   Redeploy the latest commit.

### Gmail authorization errors

-   Confirm `credentials.json` and `token.json` are present at the paths
    expected by `send_email.py`.
-   Confirm the Gmail API is enabled and the token has the
    `https://www.googleapis.com/auth/gmail.send` scope.
-   If the refresh token was revoked or expired, repeat authorization
    and securely update the deployed token file.

### Styling not appearing

-   For Gradio 6, pass CSS and JavaScript to
    `demo.launch(css=CSS, js=JS)` rather than the `Blocks` constructor.
-   If some styles still do not apply, review the CSS selectors against
    the HTML structure generated by the installed Gradio version.

## Acknowledgements

Learning Agentic AI with **Ed Donner** and applying those concepts in a
hands-on project.

------------------------------------------------------------------------

Built as a learning project to explore agentic workflows, tool calling,
external API integration, OAuth, and deployment.
