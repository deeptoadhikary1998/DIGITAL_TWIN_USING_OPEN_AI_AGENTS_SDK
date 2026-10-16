
import os
import uuid
import gradio as gr
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from styles import CSS, JS, EXAMPLES
from context import TWIN_SYSTEM_PROMPT

load_dotenv(override=True)

# 1. Configure DeepSeek
deepseek_client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)

deepseek_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=deepseek_client,
)

# 2. Create the agent
agent = Agent(
    name="DIGITAL_TWIN",
    instructions=f"""
    You are a digital twin based on the provided resume
    and LinkedIn summary.

    Answer questions using the available context.

    If you cannot answer because required information is
    missing, call note_unknown_questions with the user's
    original question.

    Collect email addresses only when explicitly requested.

    If any user asks for your email, use the collect_emails tool to record it.

    If any user expresses interest in getting in touch, ask for their email and use the collect_emails tool to record it.
    {TWIN_SYSTEM_PROMPT}
    """,
    model=deepseek_model,
    tools=[note_unknown_questions, collect_emails],
)

# 3. One SQLite session per Gradio session
# 4. Async chat function
async def chat(message, history, session_id):
    session = SQLiteSession(
        session_id,
        "digital_twin_sessions.db",
    )

    result = await Runner.run(
        agent,
        message,
        session=session,
    )

    return result.final_output


def create_session_id():
    return uuid.uuid4().hex

# Step 2: Create the Gradio app
with gr.Blocks() as demo:

    # Step 3: Store one ID for each Gradio session
    session_id = gr.State(value=create_session_id)

    # Step 4: Create the chat interface
    gr.ChatInterface(
        fn=chat,
        additional_inputs=[session_id],
        title="Digital Twin",
        description="Talk to my AI twin about my career",
    )

# Step 5: Start the app
if __name__ == "__main__":
    demo.launch()