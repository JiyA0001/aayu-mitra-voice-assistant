# utils/device_id.py
import os
import uuid
from dotenv import load_dotenv

DEVICE_FILE = "device_id.txt"

def get_device_id():
    load_dotenv()
    env_pi = os.getenv("PI_ID")
    if env_pi:
        return env_pi.strip()
    if os.path.exists(DEVICE_FILE):
        with open(DEVICE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    new_id = f"pi-{uuid.uuid4().hex[:8]}"
    with open(DEVICE_FILE, "w", encoding="utf-8") as f:
        f.write(new_id)
    return new_id

if __name__ == "__main__":
    print("Generated Device ID:", get_device_id())
