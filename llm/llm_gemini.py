import os
os.environ["GRPC_DNS_RESOLVER"] = "native"
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model = genai.GenerativeModel('gemini-1.5-pro')
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_reply(user_input, system_prompt=None, history=None):
    """
    Generate a reply using Gemini with optional system prompt and conversation history.

    Args:
        user_input (str): The latest user message.
        system_prompt (str | None): Optional system instruction to steer behavior.
        history (list[tuple[str, str]] | None): Optional prior turns as (user, assistant).

    Returns:
        str: The assistant's reply text.
    """

    # Use a per-call model if a system prompt is provided so it becomes the system instruction.
    active_model = (
        genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
        if system_prompt else
        model
    )

    gemini_history = []
    if history:
        for prev_user, prev_assistant in history:
            if prev_user:
                gemini_history.append({"role": "user", "parts": [str(prev_user)]})
            if prev_assistant:
                gemini_history.append({"role": "model", "parts": [str(prev_assistant)]})

    chat = active_model.start_chat(history=gemini_history)
    response = chat.send_message(str(user_input))
    return response.text.strip()