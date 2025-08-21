# context_logger.py
import json

CONTEXT_FILE = "context_log.jsonl"

def log_message(role, text):
    data = {"role": role, "text": text}
    with open(CONTEXT_FILE, "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")
