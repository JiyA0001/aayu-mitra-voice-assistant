import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_reply_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",  # or "gpt-4"
            model="gpt-5.1",  # or "gpt-4"
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ OpenAI Error: {str(e)}"
