import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_groq_reply(user_text, system_prompt=None):
    full_messages = []
    if system_prompt:
        full_messages.append({"role":"system","content":system_prompt})
    full_messages.append({"role":"user","content":user_text})
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=full_messages,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
