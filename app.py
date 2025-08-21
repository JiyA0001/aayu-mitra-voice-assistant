from llm.emotion_model import get_emotional_reply
from config import LLM_MODE

def main():
    print("🧠 Elderly Assistant with LLM Integration")
    while True:
        user_input = input("\n👵 User says: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # lang detection
        lang = "hi" if any(ord(c) > 128 for c in user_input) else "en"

        # Change mode here
        mode = "local"   # or "local"

        reply = get_emotional_reply(user_input, lang=lang, mode=LLM_MODE)
        print("🤖 Assistant:", reply)


if __name__ == "__main__":
    main()

