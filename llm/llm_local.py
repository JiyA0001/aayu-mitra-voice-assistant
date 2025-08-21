import requests
import ollama
# def get_reply_local(prompt):
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={"model": "gemma:2b", "prompt": prompt, "stream": False}
#         )
#         return response.json().get("response", "").strip()
#     except Exception as e:
#         return f"❌ Local LLM Error: {str(e)}"


def get_reply_local(system_prompt, user_input):
    full_prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )
    return response['message']['content'].strip()
