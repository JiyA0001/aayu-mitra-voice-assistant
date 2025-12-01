import json
from llm.llm_openai import get_reply_openai
# from llm.llm_local import get_reply_local
# from llm.llm_gemini import get_gemini_reply
from llm.llm_groq import get_groq_reply
# from llm.emotion_model import build_prompt
from config import LLM_MODE
import os

def build_prompt(user_input, lang="hi", history=None):
    import json
    import os

    # Load system prompt from file
    system_file = f"llm/system_prompt_{lang}.txt"
    with open(system_file, encoding='utf-8') as f:
        system_intro = f.read().strip() + "\n\n"

    # Load few-shot examples
    sample_file = f"datasets/emotion_samples_{lang}.jsonl"
    if not os.path.exists(sample_file):
        raise FileNotFoundError(f"Missing prompt examples at {sample_file}")

    examples = []
    with open(sample_file, encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line.strip()))

    # Build few-shot prompt
    prompt = system_intro
    # for ex in examples:
    #     prompt += f"उपयोगकर्ता: {ex['user']}\nसहायक: {ex['assistant']}\n\n" if lang == "hi" \
    #            else f"User: {ex['user']}\nAssistant: {ex['assistant']}\n\n"

    # Add conversation history
    if history:
        for prev_user, prev_assistant in history:
            prompt += f"उपयोगकर्ता: {prev_user}\nसहायक: {prev_assistant}\n\n" if lang == "hi" \
                   else f"User: {prev_user}\nAssistant: {prev_assistant}\n\n"

    prompt += f"उपयोगकर्ता: {user_input}\nसहायक:" if lang == "hi" \
           else f"User: {user_input}\nAssistant:"

    print("\n--- DEBUG: GENERATED PROMPT ---")
    print(prompt)
    print("-------------------------------\n")

    return prompt


def get_emotional_reply(user_text, lang="hi", mode="openai", history=None):
    """
    Generates emotional support reply using OpenAI or local LLM.
    :param user_text: User's message (Hindi or English)
    :param lang: Language code ("hi" or "en")
    :param mode: "openai" or "local"
    :param history: List of tuples [(user, assistant), ...]
    :return: Assistant's text reply
    """
    # Load system prompt
    try:
        with open(f"llm/system_prompt_{lang}.txt", encoding='utf-8') as f:
            system_prompt = f.read().strip()
            # print(system_prompt)
    except FileNotFoundError:
        system_prompt = "You are a helpful emotional support assistant."

    # Build few-shot prompt
    prompt = build_prompt(user_text, lang, history)

    # Add system prompt to the beginning if using local
    # full_prompt = system_prompt + "\n\n" + prompt if mode == "local" else prompt
    # print(full_prompt)

    if mode == "openai":
        return get_reply_openai(prompt)
    elif mode == "groq":
        return get_groq_reply(user_text, system_prompt, history)
    # elif mode == "local":
        # return get_reply_local(prompt)
        # return get_reply_local(system_prompt, user_text)
    # elif mode == "gemini":
    #     return get_gemini_reply(user_text, system_prompt)

    else:
        return "⚠️ Invalid mode selected."