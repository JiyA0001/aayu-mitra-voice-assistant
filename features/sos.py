# features/sos.py

import datetime

# Keywords that will trigger an SOS alert
SOS_KEYWORDS = ["help", "emergency", "save me", "बचाओ", "मदद", "सहायता", "बचाइए"]

# Function to detect if any SOS keyword is present
def detect_sos(text: str) -> bool:
    text_lower = text.lower()
    for keyword in SOS_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

# Function to log or handle the alert
def trigger_emergency_alert(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("sos_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] SOS Triggered: {message}\n")
    print("🔔 Emergency logged! Please check the logs or notify a caregiver.")
