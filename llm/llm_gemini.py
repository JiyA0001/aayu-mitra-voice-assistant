import os
os.environ["GRPC_DNS_RESOLVER"] = "native"
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-pro')
model = genai.GenerativeModel('gemini-2.0-flash-lite')

def get_gemini_reply(user_input, system_prompt=None):
    chat = model.start_chat(history=[])
    prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
    response = chat.send_message(prompt)
    return response.text.strip()